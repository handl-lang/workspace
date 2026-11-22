# workflows/lib — reusable gate fragments

Peregrin node fragments (`*.node.yml`) that campaigns `include:` to
compose language-family gates without duplicating shell. This is the
"put the behavior in the workflow" layer: the *recipes* live here
once; each campaign supplies the event contract (`on:`/`emits:`/
`params.emit`) and per-run params.

## Fragments

| File | Family | Recipe |
|---|---|---|
| `rust-gate.node.yml` | `rust` | `cargo fmt --check` → `clippy -D warnings` → `test --workspace` |
| `python-gate.node.yml` | `python` | `uv sync` → `ruff check` → `ruff format --check` → `pytest` (if tests exist) |
| `handl-gate.node.yml` | `handl` | repo's `ci.sh` if present, else `hnl typecheck/lint/test` over `handl-packages`/`src` |

## Contract

- **Parent owns events** — fragments declare no `on:`/`emits:`;
  the including node sets them plus `params.emit` (exit-code →
  event map).
- **`params.family` guard** — set it to the family name and the
  node no-ops (exit 0, no results record) on mismatch; empty runs
  unconditionally. Lets one campaign fan out all three lanes and
  select by config.
- **`params.results`** — JSONL path; every real run appends
  `{"family","repo","rc","secs"}`. Skipped lanes write nothing.
- **`params.repo`** — absolute checkout path (dev checkout;
  worktree/sibling plumbing stays in `ci.sh`/bupha land).

## Consumers

- [`../repo-verify/`](../repo-verify/) — reference consumer:
  one repo × one family, guard → 3 lanes → join → report.

## Boundary vs ci.sh

`ci.sh` remains the **per-push contract** — bupha execs it inside a
detached worktree of the pushed sha, so the gate must be committed
in the repo at that sha. These fragments serve **campaign-side**
verification (ad-hoc, sweeps, repos without ci.sh) and encode the
*baseline* recipe; repos with bespoke gates keep ci.sh and both
paths stay honest about which gate they ran.
