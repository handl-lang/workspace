<!-- myco:agent-awareness -->

## Agent awareness

- Session start / any work discussion: run `myco status --prompt`
  before proposing next steps — know the board first.
- User describes new work → offer to capture it (`myco todo add`,
  `issue new`, `proposal new`). Don't wait to be asked.
- Picking up a task: `myco resume <ID>` is the briefing.
- Wrapping up: `myco handoff <ID>` anything resumable; keep statuses
  honest (claimed → in-progress → blocked/done).

<!-- /myco:agent-awareness -->

## Global rules (propagated from ~/.config/devin/AGENTS.md)

### Public actions — ask first

Never post under the user's identity without showing the exact text and
getting approval: GitHub issues/PRs/comments, forums, chat, email — any
external service. This applies to subagents too (draft ok, publish no).
A "go" on a todo item is not approval to publish. No standalone repro,
no bug report — keep it as a TODO until one exists.

### Publishing

Never publish crates to crates.io except `tamias`. All other repos
stay git/path deps — no `cargo publish`, no release uploads.

### Mechanical changes — script them

When a change is mechanical (the same edit across many files, renames,
bulk rewrites, generated-file syncs), write a small script instead of
hand-editing. The script must be dry-runnable — a `--dry-run` flag or
no-write default that prints the planned diff — and fast + idempotent
enough to re-run safely. Review the dry-run output, then apply.

### Repo deletion checklist

Verify before deleting a local clone: no unpushed commits on any
branch (`git log --branches --not --remotes`), `status -uall`
clean (incl. `.env*`), `stash list` empty, `worktree list` (linked
checkouts elsewhere), no nested `.git` dirs, no extra remotes.

## What this repo is

Org-level home for `handl-lang/*` repos: templates, vendored gate
tooling, shared agent automation, and the gate-workflow bundle source.
It is meta — it ships conventions and CI wiring into sibling repos, it
does not build a product.

## Layout

| path | role |
| --- | --- |
| `templates/README/` | README skeletons per repo family (`engine`, `tool-compile`, `tool-codegen`, `tool`, `lib`, `kit`, `host`, `pitch`, `python`, `bare` + transitional variants) and the index with rules |
| `templates/xtask/` | vendored `cargo xtask` crate copied into Rust repos |
| `templates/gate.py` | vendored python gate (`uv run scripts/gate.py`) |
| `skills/` | org-wide agent skills (`workspace-structure`, `write-adr`); consumed via `.agents/skills/` symlinks or copies in each repo |
| `scripts/` | cross-repo shell/python gates (`check-engines`, `clone-gate`, `manifest-gate`, `prune-patches`, `sweep-deps`) |
| `workflows/` | the `handl-gates`/`tamias` campaign bundle source (`gate.yaml` is this repo's own per-push gate; `gates/`, `lib/`, `repo-verify/`, `handl-verify/`, `mlopt-nightly/` are the campaign definitions) |
| `renames/RUNBOOK.md` | repo rename procedure + deferred GH ops |
| `audit-2026-11-20.md` | repo-family consistency audit (reference) |
| `specs/` | org specs |

## Conventions

- Canonical README rules live in `templates/README/README.md`:
  MIT-only, no provenance, docs = bare link, manifest metadata
  requirements.
- Sibling repos vendor `templates/xtask` + `workflows/gate.yaml` — when
  the gate shape changes, update the template AND re-vendor into the
  affected repos (fleet-wide mechanical change → script it).
- See `templates/README/README.md` for the canonical rules and the
  family index.

## Verification

```bash
bash scripts/check-engines.sh     # engine-family consistency checks
bash scripts/manifest-gate.sh     # manifest metadata gate
bash scripts/clone-gate.sh        # fresh-clone build check
python3 scripts/prune-patches.py  # [patch] table hygiene
```
