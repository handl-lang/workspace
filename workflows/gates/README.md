# gates/ — one-shot per-family gate campaigns

Three minimal campaigns, one per language family, each gating **one**
repo checkout end-to-end:

| File | Family | Fragment | Terminal verdict |
|---|---|---|---|
| `rust.yaml` | `rust` | `../lib/rust-gate.node.yml` | `gate.pass` / `gate.fail` |
| `python.yaml` | `python` | `../lib/python-gate.node.yml` | `gate.pass` / `gate.fail` |
| `handl.yaml` | `handl` | `../lib/handl-gate.node.yml` | `gate.pass` / `gate.fail` |

Each is four nodes: `gate.init` (validate the repo target —
`GATE_REPO` env or `config.gate.repo`, truncate the results JSONL)
→ `gate.ensure`
(`../lib/ensure-siblings.node.yml` — worktree sibling layout +
shared `CARGO_TARGET_DIR` env file; no-op in a main checkout) → the
family fragment → `gate.report` (reads the `results.jsonl` record,
emits `gate.pass` on `rc == 0`, `gate.fail` otherwise). A top-level
`result:` block maps the verdict events to run conclusions
(`gate.pass`→`success`; `gate.fail`/`gate.failed`/`gate.init.failed`/
`ensure.failed`→`failure`) for `campaign run --result`. On demand
only — `on: [start]`, no schedule, no ingress.

## Run

From this checkout:

```sh
GATE_REPO=$HOME/GitHub/handl-lang/lib-command \
  ~/.local/bin/peregrin campaign run gates/rust.yaml --history run.jsonl
```

From an installed bundle the same file resolves via the store
(`tamias install ./workflows` → `handl-gates@<ver>`); per-repo
`workflows/gate.yaml` files include it as
`tamias:handl-gates@<ver>//gates/<family>.yaml`. `campaign run` is
the operator interface — `campaign submit` can't carry `GATE_*` env
vars to the server, so submitted runs need `config.gate.repo` pinned
in the served yaml instead.

`campaign run`/`submit` do not gate on node failure — the verdict is
the `gate.pass`/`gate.fail` event in the run's event log
(`--history` JSONL, `peregrin runs`/`log`).

## Knobs (env ↔ `config.gate.*`)

Every `${config.gate.*}` lookup carries an `env()` fallback:
`campaign run` reads the `GATE_*` env vars (declared in
`capabilities.env`); a served/rendered campaign can instead pin
literal values under `config.gate.*` — **config wins over env()**.

| Env | Config | Default |
|---|---|---|
| `GATE_REPO` | `gate.repo` | *(required — absolute checkout path)* |
| `GATE_RESULTS` | `gate.results` | `~/.local/share/handl-gates/<family>.results.jsonl` |
| `GATE_EXTRA` | rust only — extra `cargo test` args | `""` |
| `GATE_PYTEST_ARGS` | python only — pytest args | `-q` |
| `GATE_HNL` / `GATE_HNL_EXT_DIR` | handl only — hnl binary + ext dir | dogfood release build (same as handl-verify) |
| `GATE_SRC_DIR` | handl only — fallback source root | `""` (auto: `handl-packages` → `src`) |
| `GATE_TARGET_DIR` | all — `CARGO_TARGET_DIR` for the env file | `"auto"` (`$WORKSPACE_ROOT/.ci-target/<repo>`); `""` skips |
| `GATE_ENV_FILE` | all — where the env file lands / gate sources it | `"auto"` (`$(dirname <repo>)/.gate-env/<checkout>.env`); `""` skips |

## Per-push use (the ci.sh replacement)

These campaigns are the **reference consumers**; repos carry a
thin committed `workflows/gate.yaml` that includes the whole family
campaign — that file is the extension point (family params, extra
legs, repo-specific config via local `config:` keys, which win over
the include on merge) and keeps the gate inside the pushed sha,
same contract `ci.sh` had:

```yaml
# <repo>/workflows/gate.yaml — committed per-push gate
# (generated form — see the handl-lang/*/workflows/gate.yaml files)
include: tamias:handl-gates@0.2.0//gates/rust.yaml
```

then `GATE_REPO=$PWD GATE_RESULTS=$PWD/.gate-results.jsonl
peregrin campaign run workflows/gate.yaml --result .ci-result.json`
— `.ci-result.json`'s `conclusion` (`success`/`failure`) is the
machine verdict bupha's runner cmd checks with `jq -e`.

The `tamias:handl-gates@<ver>//<path>` include ref resolves inside
the installed bundle store (store-first, fetch-on-miss) — see
[`../lib/README.md`](../lib/README.md) for the fragment contract and
[`../repo-verify/`](../repo-verify/) for the multi-lane composition
pattern.
