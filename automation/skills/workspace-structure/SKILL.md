---
name: workspace-structure
description: Workspace structure rules for the Handl platform. Use when modifying workspace-level configuration, project layout, or Cargo.toml files.
---

# Workspace Structure

The platform is a **family of sibling git repos** under `handl-lang/` (one
clone per repo — there is no monorepo workspace). Each repo is its own Rust
workspace or pure-handl package tree; cross-repo deps float on `main` via git
deps and are `[patch]`'d to the local sibling checkouts for dev (CI strips the
patches). Repo families:

- `host` — the main workspace: `crates/` holds `platform` (the plugin
  substrate: `Plugin`/`Operation`/`Behavior`/`RuleAcceptor`/`Contribution`),
  `plugin-ext-*` (CLI extension crates), `plugin-lib-*` (native
  `Module`/`Function` impls), `plugin-sdkgen*`, `plugin-ffi`,
  `handl-runtime`, `handl-kit-*`, `handl-test-utils`, `host-tooling`.
  Root `Cargo.toml` lists members explicitly.
- `kernel` — the calculus kernel: `handl-language` (`Term`/`Language` data
  schema), `handl-value` (`Value` shapes), `handl-calculus`, `handl-ops`,
  `handl-ext`, `ops`/`prim`/`prim-handl`/`defining-handl`.
- `engine` — the `hnl-engine` umbrella. Each engine is **its own repo**:
  `engine-lex*`, `engine-parse*`, `engine-exec*` (tree-walk, bytecode,
  cranelift), `engine-typecheck*` (handl, nbe), `engine-fmt`, `engine-lint`,
  `engine-test`, `engine-transform*`, `engine-compile-*`. Engines are generic
  and data-driven — dispatch on `lang.eval`/`lang.types`/`lang.grammar`, never
  a Rust `match` on node-kind strings.
- `kit-prelude` — the canonical kit: a `Kit` wrapper over the assembled
  `Language`.
- `kit-prelude-lang` — the canonical language **as data**: YAML fragments
  (`data/ast.yaml`, `eval.yaml`, `types.yaml`, `grammar.yaml`,
  `lexer_rules.yaml`, `tokens.yaml`, `transforms.yaml`, `value_types.yaml`,
  `representations.yaml`, `caps.yaml`, `capabilities.yaml`, `globals.yaml`,
  `options.yaml`). Language changes are YAML edits, never engine edits.
- `kit-data-prelude` — `handl-kit-data-prelude` crate: kit manifests
  (`data/kits/*.yaml`), `lints.yaml`, `lsp.yaml`.
- `lib-*` — pure-handl libraries (`src/*.hnl` + `pkg.hnl`); `kit-*` — kit
  libraries; `tool-*` — tools; `ext-*` — CLI extension crates consumed by
  `host-cli`.
- `host-cli` — the `hnl` binary (a dumb ext host; commands are dynamically
  loaded `ext-*` cdylibs). `host-lsp` — LSP crates. `docs` — the docs site.
- `workspace` — org-level repo: `automation/` holds the shared agent
  skills and cross-repo tooling (merged from the retired
  `handl-lang/automation` repo), plus templates and gate workflows.
- `project/` — in each repo, a **git worktree** of that repo's `project`
  branch (gitignored on `main`, ADR-0129): `adrs/`, `notes/`, `tasks/`,
  `design/`.

## Import resolution

- `from "<spec>" import ...` — file specs resolve relative to the importing
  module's dir, then `module_root`, then CWD; a directory resolves to its
  `index.hnl` (or `<name>.hnl`); bare names fall through to the host module
  chain.

## Dependency direction

- Engines/tooling are generic and data-driven; backend-specific knowledge
  lives in the corresponding `*-backend-*`/`plugin-lib-*` crate — never leak
  it into shared IR or engines.
- `.hnl` packages stay pure handl unless the piece is an irreducible atom;
  atoms are tiny natives, everything else is handl.

## Adding things

- New Rust crate: its own repo under `handl-lang/` (or `crates/<name>` +
  workspace `members` entry inside `host`), path/git deps per the float-on-
  `main` policy.
- New stdlib/kit package: `.hnl` source in the owning `lib-*`/`kit-*` repo +
  registration in the kit manifest / `ModuleSpec`.
- New language construct: YAML fragment in `kit-prelude-lang/data/`, never an
  engine `match`.
