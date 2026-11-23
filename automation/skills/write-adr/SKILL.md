---
name: write-adr
description: How to write Architecture Decision Records for the Peregrin project. Use when making non-obvious design decisions, architecture changes, or banning patterns.
---

# Write an ADR

## When to write

- A non-obvious design choice is made.
- A pattern is banned or required.
- A dependency or tool changes.

## Structure

Start from `project/adrs/TEMPLATE.md` (in `host`). An ADR is one page:

```
project/adrs/NNNN-title.md
  ---
  title / type: adr / date / status / applies_to / refs   (YAML, ADR-0163)
  ---
  # ADR-NNNN: <decision, stated as a fact>
  ## Decision     ≤10 numbered, normative rules
  ## Why          the failure this prevents — the memory, never trimmed
  ## Not doing    rejected alternatives, one line each + why
  ## Consequences ≤5 bullets, costs included
  ## Enforcement  the file/test where this is true, or "none — proposed"
  ## Revisit if   a concrete trigger
```

The metadata is the header, not body bullets: `status` is one of `proposed`,
`accepted`, `implemented`, `landed`, `superseded`, `absorbed`, `rejected`,
`unrecorded`; a supersession is a **link, not a sentence** — `superseded_by`
names the successor, the replaced record lists `supersedes`, and no
`Superseded by ADR-N` prose survives in the body or in `status_note`. The date
lives **only** in the frontmatter — never in the filename and never as a
`- Date:` bullet. Status lives **only** in the header too: no `## Status`
section and no `Status:` line in the body; rationale, when it says more than
the enum, is `status_note`. `scripts/project-frontmatter.py` checks it.

**Budget (ADR-0161): ~8 KB, ≤10 rules.** Design detail, crate trees, phase
plans and code shapes do not go in an ADR — they go to `project/design/`,
`project/TODO.md` or `project/tasks/`. If you are writing a second page, you
are writing a design doc; link it instead.

`## Why` and `## Not doing` are the point of the record: they are what stop a
rejected design being re-proposed and the same mistake being made twice.
Without them the ADR is just a changelog entry.

Run `python3 host/scripts/check-adrs.py` before committing; a PR that adds or
changes an ADR must pass `--strict`.

`project/` is a git worktree of the repo's `project` branch (ADR-0129), not a
tracked directory on `main`. Write the file where the worktree is mounted.

## Numbers

- **Allocate the number from `project/adrs/INDEX.md`** — the global registry.
  Take the first free number; add the row in the same change.
- **Never renumber or reuse** an ADR number. It is the ADR's identifier and is
  cited from `README`, `AGENTS.md`, and code comments. Historical collisions
  are recorded as-is.
- Numbers are globally unique across the org's repos, even though each repo
  holds its own ADR files. An ADR that defines a port/kernel/composition
  decision stays in `host`; a repo-local decision lives in that repo.

## Steps

1. Allocate the next free number in `project/adrs/INDEX.md`.
2. Create `project/adrs/NNNN-title.md`.
3. Explain context, decision, and consequences.
4. Set `status` in the frontmatter to `proposed`, `accepted`, `implemented`,
   `landed`, `superseded`, `absorbed` or `rejected`.
5. Reference the ADR from `rules/` or `.windsurfrules` if it introduces a rule.
