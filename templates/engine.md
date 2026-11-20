# {{REPO_NAME}}

{{ONE_LINE_DESCRIPTION}}

{{FAMILY_BLURB}}  <!-- e.g. "`hnl-engine-lex` — the abstraction crate for the lex operation." — what makes an engine-* crate an engine-* crate -->

## Development

```bash
cargo fmt --check && cargo clippy --all-targets -- -D warnings && cargo test
```

`ci.sh` is the gate (fmt → clippy → test → doc). Deps resolve from git, so no
sibling checkouts are needed; a plain clone test-runs as-is.

## License

MIT.

## Documentation

<https://handl-lang.github.io/docs/{{DOCS_SLUG}}/>
