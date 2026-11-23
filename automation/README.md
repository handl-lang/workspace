# automation

Agent setup for the `handl-lang` org — the skills, conventions, and rules
shared across the sibling repos (`host`, `kernel`, `engine-*`, `kit-*`, …).

This directory is the **source of truth for generic agent knowledge**. A
skill belongs here when it describes a convention that applies to more than
one repo; it belongs in that repo's `.agents/skills/` when it is repo-specific.

It was merged from the standalone `handl-lang/automation` repo into
`handl-lang/workspace` (the org-config repo); the old repo is retired.

## Layout

```
skills/<name>/SKILL.md     # one directory per skill (same layout as
                           # `skills-lock.json` skillPath entries)
scripts/                    # cross-repo shell/python gates
                           # (check-engines, clone-gate, manifest-gate,
                           # prune-patches)
```

## Skills

| skill | scope |
|---|---|
| [`workspace-structure`](skills/workspace-structure/SKILL.md) | layout, import resolution, dependency direction, "adding things" |
| [`write-adr`](skills/write-adr/SKILL.md) | ADR structure and status; allocate the number from `project/adrs/INDEX.md`, never renumber (ADR-0129) |

## Using these skills from a repo

Skills are consumed by an agent from the repo's own `.agents/skills/`
directory. Either

- link a skill in: `ln -s ../../../workspace/automation/skills/write-adr .agents/skills/write-adr`
  (the target is resolved from `.agents/skills/`; a sibling `../workspace`
  checkout, the same local-dev assumption the `[patch]` tables already make), or
- copy it, if the repo must build without the sibling checkout.

Repo-specific skills (`ci-cd`, `testing`, `git-conventions`,
`create-package`, `frontend-design`, …) stay in the consuming repo.

## License

MIT (see `LICENSE` in this directory; the workspace root `LICENSE` is the
same grant).
