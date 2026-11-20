# {{REPO_NAME}}

{{DESCRIPTION_PARAGRAPH}}

## Layout

```text
{{TREE}}  <!-- crates/, src/, modules/ — one line per top-level entry -->
```

## Development

```bash
cargo fmt --check && cargo clippy --all-targets -- -D warnings && cargo test
```

`ci.sh` is the gate (fmt → clippy → test → doc). Sibling deps are git
dependencies (`branch = "main"`); the workspace-root `[patch]` tables resolve
them from sibling checkouts for local development.

## License

MIT.

## Documentation

<https://handl-lang.github.io/docs/{{DOCS_SLUG}}/>
