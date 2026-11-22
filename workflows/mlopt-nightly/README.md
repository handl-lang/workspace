# mlopt-nightly

Nightly (and on-demand) heavy lanes for `handl-lang/research-mlopt`,
as a peregrin campaign bundle (`type: peregrin-bundle`).

## What it does

Two independent chains on the same trigger:

1. `mlopt.ci.schedule` / `mlopt.bench.schedule` — cron triggers
   (staggered, UTC; `mlopt.ci_cron` / `mlopt.bench_cron`).
2. `mlopt.ci` — `uv sync --frozen` + `MLOPT_GATES_LANE=<suite_lane>
   bash scripts/gates.sh` — the Python **suite** lane that used to
   ride the per-push bupha cmd. Per-push keeps only the `static`
   lane inside `ci.sh`.
3. `mlopt.bench` — `bash scripts/bench.sh` — the ladder that used to
   be `.github/workflows/bench.yml` (uv sync + CPU torch +
   run-all/dashboard/gate; stages are non-blocking by design).
4. `mlopt.join` — `fan_in` over both lanes' `mlopt.lane.done`.
5. `mlopt.report` — summarizes `results.jsonl`, fails the run if any
   lane went red.

## Run it

```bash
# on-demand (same pipeline as the cron path — `start` walks it)
peregrin campaign run main.yaml

# or after `tamias install ./mlopt-nightly && tamias deploy mlopt-nightly`:
peregrin campaign submit --bundle mlopt-nightly
```

## Knobs (config.mlopt.*)

| key | default | meaning |
|---|---|---|
| `repo` | `~/GitHub/handl-lang/research-mlopt` | checkout the lanes run in |
| `ci_cron` / `bench_cron` | `23 4 * * *` / `47 4 * * *` | UTC schedules |
| `suite_lane` | `full` | gates.sh lane — `full` nightly, `dev` for not-slow |
| `suite_np` | `1` | pytest xdist workers (serial — memory-bound box) |
| `bench_quick` | `1` | `--quick` sweeps; `0` for deep manual runs |
| `bench_suites` | `""` | comma-separated `--suites` filter |
| `results_dir` | `~/.local/share/mlopt-nightly` | results.jsonl / summary.txt |

Env overrides (`MLOPT_*`) feed the same keys via `env()` on
`campaign run`; edit the rendered `~/.config/peregrin/serve/
mlopt-nightly.yaml` `config:` block for the deployed campaign.

## Notes

- Lanes run in the **dev checkout** — `gates.sh`/`bench.sh` are not
  worktree-safe by design (.venv, inductor cache, bench/results).
- The suite lane is hours-scale serial (`MLOPT_GATES_NP=1`); the
  node timeout is 8h. A lane that dies mid-run emits no
  `mlopt.lane.done` and the join waits — check the run log.
- bench stages never fail the lane (non-blocking, same as the retired
  GHA workflow); only env breakage (uv sync / torch install) does.
