# gates/ — one-shot per-family gate campaigns

Three minimal campaigns, one per language family, each gating **one**
repo checkout end-to-end:

| File | Family | Fragment | Terminal verdict |
|---|---|---|---|
| `rust.yaml` | `rust` | `../lib/rust-gate.node.yml` | `gate.pass` / `gate.fail` |
| `python.yaml` | `python` | `../lib/python-gate.node.yml` | `gate.pass` / `gate.fail` |
| `handl.yaml` | `handl` | `../lib/handl-gate.node.yml` | `gate.pass` / `gate.fail` |

Each is three nodes: `gate.init` (validate `config.gate.repo`,
truncate the results JSONL) → the family fragment → `gate.report`
(reads the `results.jsonl` record, emits `gate.pass` on `rc == 0`,
`gate.fail` otherwise). On demand only — `on: [start]`, no schedule,
no ingress.

## Run

From this checkout:

```sh
GATE_REPO=$HOME/GitHub/handl-lang/lib-command \
  ~/.local/bin/peregrin campaign run gates/rust.yaml --history run.jsonl
```

From an installed bundle (`tamias install ./workflows` — the whole
`workflows/` dir is the `handl-gates` bundle):

```sh
~/.local/bin/peregrin campaign submit --bundle handl-gates \
  --workflow gates/handl.yaml
```

`campaign run`/`submit` do not gate on node failure — the verdict is
the `gate.pass`/`gate.fail` event in the run's event log
(`--history` JSONL, `peregrin runs`/`log`).

## Knobs (env → `config.gate.*`)

| Env | Config | Default |
|---|---|---|
| `GATE_REPO` | `gate.repo` | *(required — absolute checkout path)* |
| `GATE_RESULTS` | `gate.results` | `~/.local/share/handl-gates/<family>.results.jsonl` |
| `GATE_EXTRA` | rust only — extra `cargo test` args | `""` |
| `GATE_PYTEST_ARGS` | python only — pytest args | `-q` |
| `GATE_HNL` / `GATE_HNL_EXT_DIR` | handl only — hnl binary + ext dir | dogfood release build (same as handl-verify) |
| `GATE_SRC_DIR` | handl only — fallback source root | `""` (auto: `handl-packages` → `src`) |

## Per-push use (the ci.sh replacement)

These campaigns are the **reference consumers**; repos are expected
to carry a thin committed `workflows/gate.yaml` that includes the
fragments directly — that file is the extension point (family params,
extra legs, repo-specific config) and keeps the gate inside the
pushed sha, same contract `ci.sh` had:

```yaml
# <repo>/workflows/gate.yaml — committed per-push gate
name: gate
config:
  gate:
    repo: "${env("GATE_REPO","")}"        # bupha sets this to the worktree
    results: "${env("GATE_RESULTS","./gate.results.jsonl")}"
nodes:
  - include: tamias:handl-gates//lib/rust-gate.node.yml
    id: gate.rust
    on: [start]
    emits: [gate.done, gate.failed]
    params:
      repo: "${config.gate.repo}"
      results: "${config.gate.results}"
      emit: {"0": gate.done, default: gate.failed}
```

then `peregrin campaign run workflows/gate.yaml`. The
`tamias:handl-gates//<path>` include ref resolves inside the
installed bundle — see [`../lib/README.md`](../lib/README.md) for the
fragment contract and [`../repo-verify/`](../repo-verify/) for the
multi-lane composition pattern.
