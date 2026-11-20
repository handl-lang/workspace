# workspace

Org-level templates and vendored gate tooling for `handl-lang/*` crate repos.

- `templates/README/` — README skeletons per repo family (`engine`,
  `engine-compile`, `tool`, `tool-sdkgen`, `lib`, `kit`, `host`, `pitch`,
  `python`, `bare` + transitional variants) and the index with rules.
- `templates/xtask/` — vendored `cargo xtask` crate for Rust repos.
- `templates/gate.py` — vendored python gate (`uv run scripts/gate.py`).
- `audit-2026-11-20.md` — repo-family consistency audit (reference).
- `renames/RUNBOOK.md` — repo rename procedure + deferred GH ops.

See `templates/README/README.md` for the canonical rules (MIT-only, no
provenance, docs = bare link, manifest metadata requirements).
