# README templates

Canonical skeletons for crate-repo `README.md` files in `handl-lang/*`, plus
the vendored gate tooling each repo standardizes on. Each repo is its own git
repo; templates and tooling are rendered per repo and committed there — this
directory is the single source of truth.

## Layout

```text
{family}.md    README skeleton per repo family
xtask/         vendored `cargo xtask` crate — copy into each Rust repo
               (invoke via `cargo run --manifest-path xtask/Cargo.toml --`)
               in `.cargo/config.toml`)
gate.py        vendored python gate — copy to `scripts/gate.py` in each
               uv/python repo (`uv run scripts/gate.py`)
```

## Templates

The `prefix-*` **is** the component kind; generic family template +
specialized sub-template when a prefix grows variants (`tool.md` →
`engine-sdkgen.md`, `engine.md` → `engine-compile.md`).

| Template | Repos |
|---|---|
| `engine.md` | `engine`, `engine-*` — language-operation engines (Rust crates) |
| `engine-compile.md` | `engine-compile-*` — compiler backends/emitters; renamed from `compile-*` |
| `tool.md` | `tool-*` — CLI/dev tools |
| `engine-sdkgen.md` | `engine-sdkgen-*` — SDK/binding generators |
| `lib.md` | `lib-*` — Handl stdlib packages (**target: `.hnl` only**) |
| `lib-rust.md` | transitional — `lib-*` pure-Rust crates pending the `.hnl` migration |
| `kit.md` | `kit-*` — kit declarations, manifests-as-data (**target: `.hnl`/data only**) |
| `kit-rust.md` | transitional — `kit-*` Rust workspaces pending migration |
| `kit-python.md` | transitional — `kit-*` Python kits (torch stack); likely relocates out of `kit-*` |
| `host.md` | `host`, `host-*` — host is **distribution only** (binaries, servers) |
| `pitch.md` | `pitch-*` — Slidev decks |
| `python.md` | `eqsat`, `kernelopt`, `gamekit`, `discoverykit`, `mlopt-product`, `research-*`, misc python |
| `bare.md` | everything else — `kernel`, `egraph`, `discovery`, `docs`, `automation`, `test`, `source-onnx`, `slidev-theme-handl` (rename pending), `extension-*` |

## Pending renames (see myco P-001 / weekend epic)

- `compile-*` → `engine-compile-*` (8 repos)
- `slidev-theme` → `slidev-theme-handl`
- `mlopt` → `research-mlopt`
- `host-tensor` → not a host — target `lib-*`/`engine-*` (decision pending;
  tensor is probably `lib-tensor`-adjacent, not distribution)
- `kit-*`/`lib-*` Rust+Python crates → `.hnl`-only packages; bindings via
  `engine-sdkgen-*` where needed — refactor planned on demand, not big-bang

## Frozen

- `kernel` — solid; do not change without a great reason.

## Placeholders

`{{REPO_NAME}}` dir name · `{{ONE_LINE_DESCRIPTION}}` / `{{DESCRIPTION_PARAGRAPH}}`
from Cargo `description`/AGENTS.md · `{{FAMILY_BLURB}}` what makes the repo a
member of its prefix family · `{{TREE}}` top-level layout · `{{DOCS_SLUG}}`
docs-site slug (omit section if no site) · `{{PACKAGE}}` / `{{SRC_DIR}}` /
`{{STACK_NOTE}}` python layout · `{{OPTIONAL_EXTRA_SECTIONS}}` for `bare`.

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
- **Rust repos gate through `xtask/`** — vendor the `xtask/` crate; `ci.sh`
  calls `cargo run --manifest-path xtask/Cargo.toml -- gate` (the
  `cargo xtask` alias lives in a gitignored `.cargo/config.toml`, dev-only).
- **Python repos gate through `uv run scripts/gate.py`** — vendor `gate.py`
  as `scripts/gate.py`; `ci.sh` calls it. `--coverage` enables the coverage
  step for repos with a `fail_under` floor.
- **`kit-*`/`lib-*` target `.hnl`-only** — no Rust, no Python; interop via
  `engine-sdkgen-*` bindings (the `engine-sdkgen-*` repos are being renamed). Transitional templates stay until each repo
  migrates.

## Repo metadata (applies to every repo, not just READMEs)

- `Cargo.toml [package]`: `description`, `license = "MIT"`, `repository`,
  `homepage`/`documentation` (docs hub URL), `keywords`, `categories`,
  `readme = "README.md"` where missing.
- `pkg.hnl`: package annotation fields alongside `modules`/`deps` — schema in
  myco proposal P-001 (`name`, `description`, `license`, `keywords`,
  `homepage`; functional keys first, annotation values must not contain the
  substrings `deps`/`modules`/`entry`).
- `package.json`: `name`, `version`, `description`, `license`, `repository`,
  `homepage`.
