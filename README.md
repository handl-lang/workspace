# workspace

Org-level templates, vendored gate tooling, and shared agent automation
for `handl-lang/*` repos.

- `automation/` — merged from the retired `handl-lang/automation` repo:
  org-wide agent skills (`skills/`), cross-repo shell/python gates
  (`scripts/`), and the per-push `workflows/gate.yaml` campaign.
- `templates/README/` — README skeletons per repo family (`engine`,
  `engine-compile`, `tool`, `tool-sdkgen`, `lib`, `kit`, `host`, `pitch`,
  `python`, `bare` + transitional variants) and the index with rules.
- `templates/xtask/` — vendored `cargo xtask` crate for Rust repos.
- `templates/gate.py` — vendored python gate (`uv run scripts/gate.py`).
- `audit-2026-11-20.md` — repo-family consistency audit (reference).
- `renames/RUNBOOK.md` — repo rename procedure + deferred GH ops.

See `templates/README/README.md` for the canonical rules (MIT-only, no
provenance, docs = bare link, manifest metadata requirements).
