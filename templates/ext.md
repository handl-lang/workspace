# {{REPO_NAME}}

{{ONE_LINE_DESCRIPTION}}

{{FAMILY_BLURB}}  <!-- the `hnl <cmd>` surface this extension provides; note the
     cdylib artifact (`libhnl_ext_*.so`) and how `hnl` discovers it
     (`--ext-dir`, `$HANDL_EXT_DIR`, `~/.handl/ext/`, dev `target/debug/`) when relevant -->

## Development

```bash
cargo fmt --check && cargo clippy --all-targets -- -D warnings && cargo test
```

`ci.sh` is the gate (fmt → clippy → test → doc). The crate builds a
`cdylib` + `rlib`; `cargo test` links the `rlib` statically.

## License

MIT.

## Documentation

<https://handl-lang.github.io/docs/{{DOCS_SLUG}}/>
