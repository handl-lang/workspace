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
