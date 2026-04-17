---
name: prism-fetch-nist
description: Fetch hydrogen-atom data from NIST's static Handbook tables (which work through sandbox proxies, unlike the CGI endpoints). Used by prism-data-fetcher for P1-T* baseline data and P5-T2/T3 extended datasets. Retries with backoff, caches to disk, emits proper handoff-contract metadata.
---

# NIST Data Fetching — Hydrogen and Hydrogenic Atoms

## What works, what doesn't (learned from v3/v4)

**Works reliably:**
- NIST Handbook static tables: `https://physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable5.htm` (and tables 2/3 for wavelengths)
- NIST Technical Note 1469 (HDEL background paper)

**Commonly blocked by sandbox proxies:**
- NIST ASD CGI endpoint: `/cgi-bin/ASD/lines1.pl` — returns 503 via many proxies
- NIST HDEL CGI endpoint — same class of block

Always try the Handbook first. Only fall back to CGI if the task explicitly needs levels beyond n=5.

## Workflow

1. Use the helper script `scripts/fetch_nist.py` which handles the proven URL list, retry, cache, and SHA256 writes:

```bash
python scripts/fetch_nist.py --table hydrogen5 --out working_dir/raw_data/
```

2. Verify the response with `scripts/verify_fetch.py <path>` — checks HTTP 200, content length ≥ expected minimum, and presence of anchor strings (e.g., `"H I"` and `"Limit"` for table 5).

3. Write the sidecar `.meta.yaml` with fetch provenance per the handoff contract:

```yaml
generated_by: prism-data-fetcher
generated_at: <timestamp>
source_url: https://physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable5.htm
http_status: 200
sha256: <hash>
content_length_bytes: <n>
spec_task_id: P1-T2
retry_count: 0
```

## Rate-limit handling

- Pause 30s between fetches from the same domain.
- On HTTP 429 or 503: exponential backoff 60s, 120s, 240s (max 3 retries).
- Cache TTL: 24 hours. Re-use the cached file if sha256 matches and age < TTL.

## Citations to record

Every NIST Handbook fetch references:
- Kelleher & Podobedova, *J. Phys. Chem. Ref. Data* 37, 267 (2008), citation MK00a in the NIST compilation — based on Mohr & Kotochigova, *Phys. Rev. A* 61, 052502 (2000).

Write this citation into `working_dir/knowledge_base/citations.bib` with key `nist_handbook_hydrogen`.
