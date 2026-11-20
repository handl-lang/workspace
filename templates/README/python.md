# {{REPO_NAME}}

{{DESCRIPTION_PARAGRAPH}}

## Packages

<!-- Bullet list of shipped importable packages and what each contains.
     Omit if single-package src/ layout — describe inline instead. -->

- `{{PACKAGE}}` — {{WHAT_IT_CONTAINS}}

## Develop

```sh
uv sync --group dev
```

## Verify

```sh
uv run scripts/gate.py      # pytest → ruff → ty → lint-imports → coverage floor
```

`scripts/gate.py` is a stdlib runner over the dev toolchain; `ci.sh` is the
gate entry. Keep only the steps the repo configures (check `pyproject.toml`).

## License

MIT.

## Documentation

<https://handl-lang.github.io/docs/{{DOCS_SLUG}}/>
