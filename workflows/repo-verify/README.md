# repo-verify

Run the canonical family gate (rust / python / handl) against **one**
repo checkout. Composes the reusable fragments in
[`../lib/`](../lib/) — this bundle is the reference consumer that
proves the composition pattern.

## Run

```sh
peregrin campaign run main.yaml \
  --env REPO_VERIFY_REPO=$HOME/GitHub/handl-lang/lib-command \
  --env REPO_VERIFY_FAMILY=handl
```

`REPO_VERIFY_FAMILY` selects the lane: `rust`, `python`, `handl`, or
empty to run all three. Other knobs: `REPO_VERIFY_HNL`,
`REPO_VERIFY_HNL_EXT_DIR`, `REPO_VERIFY_RESULTS_DIR` (defaults in
`main.yaml`).

## Pipeline

```
start → verify.guard ──verify.due──▶ verify.gate.{rust,python,handl}
                                          │  (family guard no-ops
                                          │   non-selected lanes)
                                          ▼
                                    verify.gate.end ×3
                                          │  fan_in count:3
                                          ▼
                                    verify.mapped → verify.report
```

Each fragment appends `{"family","repo","rc","secs"}` to
`results.jsonl`; `verify.report` fails the campaign if any ran lane
has `rc != 0`. Skipped lanes record nothing.

## When to use which gate

| Tool | Scope | Gate source |
|---|---|---|
| `bash ci.sh` (bupha) | per-push, worktree @ sha | repo's committed script |
| `handl-verify` | fleet sweep, nightly | every repo's `ci.sh` |
| `repo-verify` + `lib/*` | one repo, ad-hoc | canonical family fragment (ci.sh preferred when present) |
| `mlopt-nightly` | research-mlopt suite+bench | `scripts/gates.sh`, `scripts/bench.sh` |
