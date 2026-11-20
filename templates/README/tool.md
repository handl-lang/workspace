# {{REPO_NAME}}

{{ONE_LINE_DESCRIPTION}}

{{FAMILY_BLURB}}  <!-- what tool this repo provides and the `hnl`/CLI surface
     it exposes -->

## Development

```bash
cargo xtask gate        # fmt --check → clippy -D warnings → test → doc
```

`cargo xtask` wraps the repo's `xtask/` crate; `ci.sh` is the gate entry.

## License

MIT.

## Documentation

<https://handl-lang.github.io/docs/{{DOCS_SLUG}}/>
