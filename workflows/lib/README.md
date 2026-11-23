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
  worktree/sibling plumbing stays in bupha land).

## Consumers

- [`../gates/`](../gates/) — one-shot per-family campaigns
  (`gate.init` → fragment → `gate.report` emitting `gate.pass`/
  `gate.fail`); the packaged form bupha-side consumers invoke.
- [`../repo-verify/`](../repo-verify/) — reference consumer:
  one repo × one family, guard → 3 lanes → join → report.

All of the above ship inside the **`handl-gates` tamias bundle**
([`../tamias.yaml`](../tamias.yaml)) — the whole `workflows/` dir is
one `peregrin-bundle` payload (`type: peregrin-bundle`,
`provider.name: peregrin`, `verbs: [run, logs]`). Repos that want a
committed per-push gate include fragments by bundle ref:
`include: tamias:handl-gates//lib/<family>-gate.node.yml`.

## Boundary vs ci.sh

`ci.sh` is being **retired** as the per-push contract — repos carry a
thin committed `workflows/gate.yaml` that composes these fragments
instead, and bupha invokes `peregrin campaign run` on it inside the
pushed worktree (same sha-commitment guarantee ci.sh had). These
fragments are now the gate *implementation*, not just the
campaign-side baseline: the recipe lives here once, per-repo
gate.yaml files only wire events/params. Repos with bespoke gates
extend via `params.extra`/`pytest_args`/`src_dir` or their own nodes;
both paths stay honest about which gate they ran.
