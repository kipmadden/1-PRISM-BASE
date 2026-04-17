---
description: Bootstrap the PRISM working directory — state files, knowledge base, source URL manifest, operator basis config. Run once at the start of a fresh research session.
argument-hint: "[working_dir_path]"
---

# Bootstrap the PRISM research working directory

Target working directory: `$1` (default: `./working_dir`)

## Steps

1. Create the directory tree:
   ```
   <working_dir>/
     raw_data/
     structured_data/
     derivations/
     predictions/
     validation/
     figures/
     diagnostics/
     knowledge_base/
     pysr_fits/
     deliverables/
     checkpoints/
   ```

2. Copy templates from the plugin's `templates/` folder into the new working directory:
   - `current_state.json` (initialized to phase 1, no task started)
   - `phase_status.json` (all phases PENDING)
   - `source_urls.yaml`
   - `operator_basis_config.yaml`
   - `handoff_contract_template.yaml`
   - `knowledge_base/literature_values.yaml` (seeded from spec Appendix A)
   - `knowledge_base/codata_2022.yaml`
   - `knowledge_base/bethe_log_literature.yaml`
   - `knowledge_base/proton_radius_puzzle.yaml`

3. Copy the research plan: `prism_research_plan_v1.0.md` (from plugin root or user upload) to working directory root.

4. If `prism_hydrogen_v4.py` is present in the user's project root, copy to `working_dir/phase_0_pipeline/` — Phase 0 is pre-complete per spec.

5. Initialize `working_dir/audit.log` with a header line.

6. Print a status block confirming the bootstrap and listing the next step: "Run `/prism-status` to see the task DAG, or `/prism-next` to dispatch P1-T1."

## Verification

Before reporting success, verify all template files copied, and that `literature_values.yaml` contains all seven required keys from Appendix A (bethe_log_values, hydrogen_lamb_shift, muonic_hydrogen_lamb_shift, proton_radius_electronic, proton_radius_muonic, alpha_at_me, alpha_at_mz).
