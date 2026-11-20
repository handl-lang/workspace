# README templates

Canonical skeletons for crate-repo `README.md` files in `handl-lang/*`.
Each repo is its own git repo; templates are rendered per repo and committed
there — this directory is the single source of truth for structure.

## Families

| Template | Use when |
|---|---|
| `rust-crate.md` | Single-crate Rust repo (`Cargo.toml`, no `crates/` workspace, no `pkg.hnl`/`handl-packages/`) — most `engine-*`, `ext-*`, `lib-*` Rust, `compile-*`, `sdkgen-*` |
| `rust-workspace.md` | Rust workspace (`crates/` members) — `kit-*` Rust, `host-cli`, `compile-handl` |
| `handl-pkg.md` | Handl package (`pkg.hnl` or `handl-packages/`) — most `lib-*` |
| `python-pkg.md` | Python/uv repo (`pyproject.toml`, no Cargo) — `eqsat`, most `kit-*` Python, `kernelopt`, `gamekit`, `discoverykit`, `mlopt-product` |
| `fallback.md` | Anything else — minimal title + desc + license |

## Placeholders

`{{REPO_NAME}}` dir name · `{{ONE_LINE_DESCRIPTION}}` / `{{DESCRIPTION_PARAGRAPH}}`
from Cargo `description`/AGENTS.md · `{{PROVENANCE_NOTE}}` ADR/split note ·
`{{TREE}}` top-level layout · `{{LICENSE}}` from LICENSE files ·
`{{DOCS_SLUG}}` docs-site slug (omit section if no site) · `{{PACKAGE}}` /
`{{SRC_DIR}}` python layout.

## Rules

- Normalize structure, keep existing prose — do not rewrite good bespoke
  sections; move/reorder to match the family skeleton.
- Omit optional sections (Documentation, Gate variant, Packages) when they
  don't apply rather than leaving placeholders.
- License: `MIT` or `MIT OR Apache-2.0` per the repo's LICENSE files.
