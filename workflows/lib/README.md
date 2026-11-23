# workflows/lib — reusable gate fragments

Peregrin node fragments (`*.node.yml`) that campaigns `include:` to
compose language-family gates without duplicating shell. This is the
"put the behavior in the workflow" layer: the *recipes* live here
once; each campaign supplies the event contract (`on:`/`emits:`/
`params.emit`) and per-run params.

## Fragments

| File | Family | Recipe |
|---|---|---|
| `ensure-siblings.node.yml` | any | worktree sibling-layout restoration (`../<repo>` self-link + sibling symlinks) + shared `CARGO_TARGET_DIR` env file — the ci.sh `ensure_siblings` port |
| `rust-gate.node.yml` | `rust` | repo's `ci.sh` if present, else `cargo fmt --check` → `clippy -D warnings` → `test --workspace` |
| `python-gate.node.yml` | `python` | repo's `ci.sh` if present, else `uv sync` → `ruff check`/`format --check` (when ruff is installed) → `pytest` (if tests exist) |
| `handl-gate.node.yml` | `handl` | repo's `ci.sh` if present, else `hnl typecheck/lint/test` over canonical-dialect `handl-packages`/`src` sources (arrow-dialect `.hnl` skipped, per `scripts/hnl-gate.sh`) |

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

## ensure-siblings.node.yml

The ci.sh `ensure_siblings` port as a composable node — run it
between `gate.init` and the family gate so push-worktree runs get
the same `../<repo>` sibling layout ci.sh used to build:

- Derives `MAIN_CHECKOUT` via `git rev-parse --git-common-dir`,
  `WORKSPACE_ROOT` as its parent, `IN_WORKTREE` by comparing the
  checkout path to the main checkout. **Main checkout = no-op**
  (exit 0) for the symlink half — the real layout is already right.
- Worktree: refuses when the worktree sits inside the workspace
  root, refuses to clobber a real (non-symlink) `../<repo>`, then
  self-links `../<repo>` → this checkout and refreshes every other
  sibling symlink. Repo name = basename of the **main checkout**
  (the name `[patch]` tables spell), not the worktree dir name.
- Env file: shell nodes can't share `export`s, so the node writes
  `export CARGO_TARGET_DIR=…` to
  `$(dirname <repo>)/.gate-env/<checkout>.env` — `params.target_dir`
  `"auto"` (default) = `$WORKSPACE_ROOT/.ci-target/<repo>`, a literal
  path overrides, `""` skips; `params.env_file` `"auto"` (default) =
  the `.gate-env/` path above, a literal path overrides, `""` skips
  the write. `rust-gate`/`python-gate` source the auto path before
  their build legs (`params.env_file` there takes the same
  auto/literal/empty convention).
- Emits `ensure.done`/`ensure.failed` via `params.emit` like every
  other fragment; gate campaigns map `ensure.failed` to a `failure`
  conclusion in their `result:` block.

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
