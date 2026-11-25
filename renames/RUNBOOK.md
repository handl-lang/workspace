# Repo rename runbook (T-109)

Local-first renames. GH repo renames + remote URL updates are deferred to
the publishing batch (T-111) — old GitHub names keep working via redirects
after rename, and git URLs in manifests can stay on old names until then.

## Rename map

| Old | New | Count |
|---|---|---|
| `sdkgen-{c,cli,file,python,webidl}` | `tool-sdkgen-{c,cli,file,python,webidl}` | 5 |
| `compile-{cuda,dot,handl,js,llvm,sexp,term,triton}` | `tool-compile-{cuda,dot,handl,js,llvm,sexp,term,triton}` | 8 |
| `slidev-theme` | `slidev-theme-handl` | 1 |
| `mlopt` | `research-mlopt` | 1 |
| `exec-tensor` | `lib-tensor-native` (done — atom provider, `lib-char-native` convention; handl/lib family) | 1 |
| `kit-torch` | `mlopt-torch` (done) | 1 |
| `kit-discovery` | `mlopt-discovery` (done) | 1 |
| `kit-carriers` | `mlopt-carriers` (done) | 1 |
| `mlopt-torch` | `kit-torch` (done — P3 completion, GH rename + remote + dep sweep) | 1 |
| `mlopt-discovery` | `kit-discovery` (done) | 1 |
| `mlopt-carriers` | `kit-carriers` (done) | 1 |
| `mlopt-product` | `kit-product` (done) | 1 |
| `mlopt-pipeline` | `kit-pipeline` (done; package stays `mlopt-pipeline`/`mlopt_pipeline` — product-facing name, kit-product precedent) | 1 |

Crate/package names inside the repos do NOT change (e.g. `hnl-sdkgen-c`,
`handl-compile-*`) — only repo dir names, git remotes, and references.

## Per-repo procedure

1. `cd <old> && git status` — must be clean.
2. `mv <old> <new>` (plain `mv` — `.git` travels).
3. `git -C <new> remote set-url origin git@github.com:handl-lang/<new>.git`
   — WAIT: the GH repo doesn't exist under the new name yet. Keep the OLD
   remote URL until the GH rename happens (it still resolves). Do NOT
   set-url yet; record it in the deferred-publish list instead.
   Actually: set-url to the NEW url is fine ONLY after `gh repo rename`.
   Before that, leave remote untouched.
4. Update references org-wide (see below), commit per repo.

## Reference sweep (the coordinated part)

`[patch]`/path deps and bupha manifests reference **dir names**, so every
sibling checkout must be updated in the same wave:

- `Cargo.toml` `[patch]` tables: `path = "../<old>"` → `"../<new>"`
  (~12 files mention sdkgen-*, ~17 compile-*)
- `[dependencies]` git URLs `github.com/handl-lang/<old>` — LEAVE (GH
  redirect post-rename; cosmetic sweep later).
- `bupha.toml`: `name = "handl-lang/<old>"` + `dir = ".../<old>"` (~13 files)
- `docs/structure.md`, `docs/scripts/gen_reference.py` prefix lists,
  `docs/scripts/public_repos.py` allowlist — update names.
- myco registry entries (`myco current list` shows registry paths) —
  re-register or update after rename.
- `.gitignore`/`ci.sh`/`AGENTS.md` self-references to repo name — update
  where they name the repo (check per repo).
- README titles already use repo name — update `# <old>` → `# <new>` in the
  renamed repos' READMEs.

## Suggested order (one family per commit wave)

1. `sdkgen-*` → `tool-sdkgen-*` (5) — smallest, validates the procedure.
2. `compile-*` → `tool-compile-*` (8).
3. `slidev-theme` → `slidev-theme-handl`, `mlopt` → `research-mlopt` (1 each).
4. `exec-tensor` — done: renamed `lib-tensor-native` (P-013 atom-provider
   convention, `lib-char-native` precedent; `handl/lib` family). Crate
   `handl-host-tensor` and PyO3 module `handl_host_tensor` names kept —
   repo name is distribution, crate name is API surface.

## Deferred to T-111 (needs user go)

- `gh repo rename handl-lang/<old> <new>` per repo (creates redirects).
- `git remote set-url` to new names + push any unpushed commits.
- Update git-URL deps org-wide to new names (cosmetic; redirects cover it).
- `workspace` repo already live; docs repo `public_repos.py` sync.

## Risks

- Missing a `[patch]` path → sibling builds break with "failed to load
  manifest" — mitigate with a post-rename `cargo metadata` spot-check on a
  few dependents per family.
- `Cargo.lock` files record old git URLs — harmless (redirects), refresh on
  next `cargo update`.
- myco registry/index paths go stale — rebuild index after renames.
