#!/usr/bin/env python3
"""
fetch_nist.py — NIST data retrieval helper for the PRISM pipeline.

Usage:
    python fetch_nist.py --source <source_key> --out <output_dir> [--force]
    python fetch_nist.py --url <full_url> --out <output_dir> --name <filename>

Behavior
--------
- Reads the source manifest from templates/source_urls.yaml (or --manifest override).
- GETs the URL with a polite User-Agent and an aggressive retry policy.
- Caches responses for 24 hours by default (override with --cache-ttl-hours).
- Writes {output_dir}/{name} and {output_dir}/{name}.meta.yaml sidecar.
- Computes SHA256 of the response body and records it in the sidecar.
- Exits 0 on success, 2 on proxy-blocked CGI endpoint, 3 on other HTTP errors.

Design notes
------------
- The NIST Handbook static HTML tables are proxy-safe and should always succeed.
- The /cgi-bin/ASD/ and /cgi-bin/HDEL/ endpoints are frequently blocked; callers
  should fall back to parsed static tables when this script returns exit 2.
- No JavaScript execution; if a target is SPA-rendered, this script WILL NOT work
  and the task must escalate to the user.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import re
import sys
import time
import urllib.request
import urllib.error

try:
    import yaml
except ImportError:
    sys.stderr.write("PyYAML not installed. Run: pip install pyyaml --break-system-packages\n")
    sys.exit(4)

USER_AGENT = "prism-base-research/0.1 (PRISM theory validation; contact kipmadden@cosapient.com)"
DEFAULT_CACHE_TTL_HOURS = 24
RETRY_BACKOFFS_SECONDS = (60, 120, 240)  # on 429/503
PROXY_BLOCKED_PATTERNS = (
    r"cgi-bin/ASD",
    r"cgi-bin/HDEL",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_cgi_endpoint(url: str) -> bool:
    return any(re.search(p, url) for p in PROXY_BLOCKED_PATTERNS)


def load_manifest(path: pathlib.Path) -> dict:
    with path.open("r") as f:
        return yaml.safe_load(f)


def cache_is_fresh(meta_path: pathlib.Path, ttl_hours: int) -> bool:
    if not meta_path.exists():
        return False
    try:
        with meta_path.open("r") as f:
            meta = yaml.safe_load(f)
        fetched = dt.datetime.fromisoformat(meta["provenance"]["fetch_timestamp"].replace("Z", "+00:00"))
        age = dt.datetime.now(dt.timezone.utc) - fetched
        return age < dt.timedelta(hours=ttl_hours)
    except Exception:
        return False


def fetch(url: str) -> bytes:
    last_err: Exception | None = None
    for attempt, backoff in enumerate([0, *RETRY_BACKOFFS_SECONDS]):
        if backoff:
            sys.stderr.write(f"[fetch_nist] retry {attempt} after {backoff}s backoff...\n")
            time.sleep(backoff)
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (429, 503):
                continue
            raise
        except urllib.error.URLError as e:
            last_err = e
            if is_cgi_endpoint(url):
                # Proxy block commonly manifests as connection refusal on CGI URLs.
                raise RuntimeError(f"CGI endpoint likely proxy-blocked: {url}") from e
            continue
    raise RuntimeError(f"Fetch failed after retries: {last_err}")


def write_artifact_with_sidecar(
    body: bytes,
    out_dir: pathlib.Path,
    filename: str,
    *,
    url: str,
    source_key: str | None,
    citation_key: str | None,
    spec_task_id: str,
) -> tuple[pathlib.Path, pathlib.Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    artifact = out_dir / filename
    sidecar = out_dir / f"{filename}.meta.yaml"
    artifact.write_bytes(body)

    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    meta = {
        "generated_by": "prism-data-fetcher",
        "generated_at": now,
        "spec_task_id": spec_task_id,
        "depends_on": [],
        "spec_version": "1.0",
        "artifact_type": "raw_fetch",
        "content_sha256": sha256_bytes(body),
        "provenance": {
            "source_citation_key": citation_key,
            "source_url": url,
            "fetch_timestamp": now,
            "upstream_chain": [f"{spec_task_id} -> {artifact.name}"],
        },
    }
    if source_key:
        meta["provenance"]["source_key"] = source_key
    with sidecar.open("w") as f:
        yaml.safe_dump(meta, f, sort_keys=False)
    return artifact, sidecar


def main() -> int:
    parser = argparse.ArgumentParser(description="NIST data fetcher for PRISM pipeline")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--source", help="key in source_urls.yaml")
    mode.add_argument("--url", help="fetch this URL directly")
    parser.add_argument("--manifest", default="templates/source_urls.yaml")
    parser.add_argument("--out", required=True)
    parser.add_argument("--name", help="output filename (required with --url)")
    parser.add_argument("--spec-task-id", default="unknown")
    parser.add_argument("--cache-ttl-hours", type=int, default=DEFAULT_CACHE_TTL_HOURS)
    parser.add_argument("--force", action="store_true", help="bypass cache")
    args = parser.parse_args()

    out_dir = pathlib.Path(args.out)
    if args.source:
        manifest = load_manifest(pathlib.Path(args.manifest))
        if args.source not in manifest:
            sys.stderr.write(f"unknown source key: {args.source}\n")
            return 5
        entry = manifest[args.source]
        url = entry.get("url")
        if not url:
            sys.stderr.write(f"source {args.source} has no url field (maybe a DOI-only paper?)\n")
            return 5
        citation_key = entry.get("citation_key")
        filename = f"{args.source}.html" if entry.get("type") == "static_html" else f"{args.source}.bin"
        source_key = args.source
    else:
        if not args.name:
            sys.stderr.write("--name required when --url is used\n")
            return 6
        url, citation_key, filename, source_key = args.url, None, args.name, None

    sidecar_path = out_dir / f"{filename}.meta.yaml"
    if not args.force and cache_is_fresh(sidecar_path, args.cache_ttl_hours):
        sys.stderr.write(f"[fetch_nist] cache hit (<{args.cache_ttl_hours}h): {out_dir / filename}\n")
        print(str(out_dir / filename))
        return 0

    try:
        body = fetch(url)
    except RuntimeError as e:
        sys.stderr.write(f"[fetch_nist] PROXY_BLOCK: {e}\n")
        return 2
    except Exception as e:
        sys.stderr.write(f"[fetch_nist] HTTP_ERROR: {e}\n")
        return 3

    artifact, sidecar = write_artifact_with_sidecar(
        body, out_dir, filename,
        url=url, source_key=source_key, citation_key=citation_key,
        spec_task_id=args.spec_task_id,
    )
    print(json.dumps({"artifact": str(artifact), "sidecar": str(sidecar), "sha256": sha256_bytes(body), "bytes": len(body)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
