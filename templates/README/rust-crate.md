# {{REPO_NAME}}

{{ONE_LINE_DESCRIPTION}}

{{PROVENANCE_NOTE}}  <!-- e.g. "Part of the stdlib → `lib-*` split (ADR-0128)." — omit if none -->

## Development

```bash
cargo fmt --check && cargo clippy --all-targets -- -D warnings && cargo test
```

`ci.sh` is the gate (fmt → clippy → test → doc). Deps resolve from git, so no
sibling checkouts are needed; a plain clone test-runs as-is.

## License

{{LICENSE}}  <!-- MIT / MIT OR Apache-2.0 — match LICENSE* files -->

## Documentation

<!-- Only when a published docs site exists for this repo. Otherwise omit the
     whole section. -->

Published site (Diátaxis): <https://handl-lang.github.io/docs/{{DOCS_SLUG}}/>

- [Reference](https://handl-lang.github.io/docs/{{DOCS_SLUG}}/reference/) — public API surface
- [How-to](https://handl-lang.github.io/docs/{{DOCS_SLUG}}/how-to/) — task recipes
- [Explanation](https://handl-lang.github.io/docs/{{DOCS_SLUG}}/explanation/) — design and rationale

Decision records live on the `project` branch under `project/adrs/`.
