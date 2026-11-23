# {{REPO_NAME}}

{{DESCRIPTION_PARAGRAPH}}

## Layout

```text
{{TREE}}  <!-- crates/, src/, modules/ — one line per top-level entry -->
```

## Development

```bash
cargo run --manifest-path xtask/Cargo.toml -- gate   # fmt → clippy → test → doc
```

`xtask/` provides the repo's `xtask/` crate; `ci.sh` is the gate entry. Sibling deps are git
dependencies (`branch = "main"`); the workspace-root `[patch]` tables resolve
them from sibling checkouts for local development.

## License

MIT.

## Documentation

<https://handl-lang.github.io/docs/{{DOCS_SLUG}}/>
