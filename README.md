# workspace

Org-level home for `handl-lang/*` repos: templates, vendored gate
tooling, shared agent automation, and the gate-workflow bundle source.

- `templates/README/` — README skeletons per repo family (`engine`,
  `engine-compile`, `engine-sdkgen`, `tool`, `lib`, `kit`, `host`,
  `pitch`, `python`, `bare` + transitional variants) and the index with rules.
- `templates/xtask/` — vendored `cargo xtask` crate for Rust repos.
- `templates/gate.py` — vendored python gate (`uv run scripts/gate.py`).
- `skills/` — org-wide agent skills (`workspace-structure`, `write-adr`);
  consumed via `.agents/skills/` symlinks or copies in each repo.
- `scripts/` — cross-repo shell/python gates (`check-engines`,
  `clone-gate`, `manifest-gate`, `prune-patches`).
- `workflows/` — the `handl-gates`/`tamias` campaign bundle source
  (`gate.yaml` is this repo's own per-push gate).
- `audit-2026-11-20.md` — repo-family consistency audit (reference).
- `renames/RUNBOOK.md` — repo rename procedure + deferred GH ops.

See `templates/README/README.md` for the canonical rules (MIT-only, no
provenance, docs = bare link, manifest metadata requirements) and
`AGENTS.md` for agent-session conventions.
