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
uv run scripts/gate.py      # pytest → ruff → ty → lint-imports → coverage floor
```

`scripts/gate.py` is a stdlib runner over the dev toolchain; `ci.sh` is the
gate entry. Keep only the steps the repo configures (check `pyproject.toml`).

## License

MIT.

## Documentation

<https://handl-lang.github.io/docs/{{DOCS_SLUG}}/>
