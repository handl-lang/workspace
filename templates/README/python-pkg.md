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
.venv/bin/python -m pytest tests/ -q
.venv/bin/ruff check {{SRC_DIR}}        # src/ or packages/
.venv/bin/ruff format --check {{SRC_DIR}}
.venv/bin/ty check
.venv/bin/lint-imports                  # only when import-linter contracts exist
coverage run -m pytest tests/ -q && coverage report -m   # only when floor set
```

<!-- Keep only the commands the repo actually has configured (check
     pyproject.toml / ci.sh). -->

## License

{{LICENSE}}

## Documentation

<!-- Only when a published docs site exists. Otherwise omit. -->

Published site (Diátaxis): <https://handl-lang.github.io/docs/{{DOCS_SLUG}}/>
