# handl-verify

Fleet-wide gate sweep for the handl-lang workspace, as a peregrin
campaign bundle (`type: peregrin-bundle`).

## What it does

1. `verify.schedule` — cron trigger (`verify.cron`, default nightly).
2. `verify.toolchain` — asserts the `hnl` binary + `libhnl_ext_*.so`
   the `lib-*` gates need exist before fan-out.
3. `verify.plan` — enumerates every `<workspace>/*/ci.sh` (minus
   `verify.skip`), slices the list into `verify.workers` chunks, and
   emits worker node specs `{nodes: [...]}`. (The enumeration key is
   still `ci.sh` presence — every gated repo ships one during the
   transition; repos that lose it should join `verify.skip`.)
4. `verify.runner` — `driver: runner` injects the specs into the live
   graph; `verify.spawned` fires them.
5. `verify.work.<i>` — one shell worker per chunk: per repo, runs
   the committed `workflows/gate.yaml` campaign
   (`GATE_REPO=$PWD GATE_RESULTS=$PWD/.gate-results.jsonl
   peregrin campaign run workflows/gate.yaml --result
   $PWD/.ci-result.json`, verdict = jq `.conclusion == "success"`)
   when present — the ci.sh replacement — else falls back to
   `timeout <gate_timeout> bash ci.sh`. Appends `{repo, rc, secs}`
   to `results.jsonl`, per-repo logs under `logs/`.
6. `verify.join` — `fan_in` over `verify.work.*.done`.
7. `verify.report` — summary counts + failing repo list →
   `summary.txt`; `verify.report.failed` if any repo failed.

## Run it

```bash
# on-demand (same pipeline as the cron path — `start` walks it)
peregrin campaign run main.yaml

# or after `tamias install ./handl-verify && tamias deploy handl-verify`:
peregrin campaign submit --bundle handl-verify   # then campaign status/events
peregrin logs runs --dir ~/.local/share/peregrin/runs
```

## Knobs (config.verify.*)

| key | default | meaning |
|---|---|---|
| `workspace` | `~/GitHub/handl-lang` | sibling checkouts root |
| `workers` | `6` | parallel gate runners — memory-bound, keep small |
| `gate_timeout` | `1800` | per-repo `timeout` around the gate (campaign run or ci.sh fallback) |
| `cron` | `37 5 * * *` | schedule driver cron |
| `hnl` / `hnl_ext_dir` | `.ci-target/dogfood/release/{hnl,…}` | toolchain the lib gates resolve |
| `results_dir` | `~/.local/share/handl-verify` | results.jsonl / plan / logs / summary |
| `skip` | `assets workspace lib-mri` | space-separated repo names to exclude |

Env overrides (`HANDL_VERIFY_*`) feed the same keys via `env()` on
`campaign run`; edit the rendered `~/.config/peregrin/serve/
handl-verify.yaml` `config:` block for the deployed campaign.

## Notes

- Workers run gates in the **dev checkout**, not a worktree —
  `IN_WORKTREE=0` makes the campaign's `gate.ensure` node a no-op
  (and ci.sh's own `ensure_siblings` likewise), and `[patch]`
  tables resolve against the real sibling layout. Results reflect
  each repo's `main` checkout state, not a pushed sha.
- bupha remains the per-push gate (`ci/bupha` statuses); this
  campaign is the cross-repo sweep/verification lane.
- A worker that dies mid-slice emits no `*.done` and the join waits —
  check `verify.work.*` node failures in the run log.
