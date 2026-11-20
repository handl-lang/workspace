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
from Cargo `description`/AGENTS.md · `{{TREE}}` top-level layout ·
`{{DOCS_SLUG}}` docs-site slug (omit section if no site) · `{{PACKAGE}}` /
`{{SRC_DIR}}` python layout.

## Rules

- **License is always MIT** — `## License` says `MIT.`; every repo must carry
  a `LICENSE` file with the MIT text.
- **No provenance** — no ADR citations, no "part of the X split", no history
  notes in READMEs.
- **Docs = one link** — `## Documentation` is a bare URL to the repo's page on
  the docs hub; the Diátaxis structure lives inside the docs site, never
  spelled out here. Omit the section when no site exists.
- Normalize structure, keep existing prose — do not rewrite good bespoke
  sections; move/reorder to match the family skeleton.
- Omit optional sections (Documentation, Gate variant, Packages) when they
  don't apply rather than leaving placeholders.

## Repo metadata (applies to every repo, not just READMEs)

- `Cargo.toml [package]`: `description`, `license = "MIT"`, `repository`,
  `homepage`/`documentation` (docs hub URL), `keywords`, `categories`,
  `readme = "README.md"` where missing.
- `pkg.hnl`: package annotation fields alongside `modules`/`deps` (schema TBD
  — see plan).
- `package.json`: `name`, `version`, `description`, `license`, `repository`,
  `homepage`.
