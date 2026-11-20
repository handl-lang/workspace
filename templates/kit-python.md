# {{REPO_NAME}}

{{DESCRIPTION_PARAGRAPH}}

{{STACK_NOTE}}  <!-- python version, torch/mlopt substrate deps, position in the
     stack (e.g. "top of the torch stack", "torch-free") when relevant -->

## Packages

<!-- Bullet list of shipped importable packages and what each contains.
     Omit if single-package src/ layout — describe inline instead. -->

- `{{PACKAGE}}` — {{WHAT_IT_CONTAINS}}

## Develop

```sh
uv sync --group dev
```

or as a git dependency:

```toml
{{REPO_NAME}} = { git = "https://github.com/handl-lang/{{REPO_NAME}}.git", tag = "v0.1.0" }
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

MIT.

## Documentation

<https://handl-lang.github.io/docs/{{DOCS_SLUG}}/>
