# Copilot instructions

This is a **Python template repository**: a starter for Python projects with standardized
configurations, tooling, and project layout that downstream projects can inherit.

Changes to shared configuration should be considered carefully and mirrored in other
repositories that use the same setup.

## Tech stack

- **Python**
- **uv** for dependency and virtualenv management
- **Task** (`Taskfile.yml`) as the command runner — preferred over invoking tools directly
- **pytest**  for tests
- **Ruff** for formatting and linting
- **ty** for type checking
- **pydantic-settings** for environment-driven configuration
- **zizmor** for GitHub Actions security checks
- Dev container support (`.devcontainer/`)

## Project layout

This uses a **flat layout** where the package itself is named `src` (see `pyproject.toml`:
`name = "src"`). Imports therefore look like `from src.settings import settings`. Do not
confuse this with the "src layout" — there is no nested package inside `src/`.

```text
src/                  # Application package (imported as `src`)
tests/                # Pytest tests (live at repo root, not under src/)
main.py               # Entry point
pyproject.toml        # Project metadata, dependencies, ruff config
Taskfile.yml          # Task commands
.env / .env.example   # Environment variables (loaded automatically by Taskfile + pydantic)
```

## Running commands

Always prefer `task <name>` over running tools directly. Common tasks:

- `task run` — run `main.py`
- `task install` — `uv sync --dev`
- `task test` — `uv run pytest`
- `task check` — `uvx ty check` (type checking)
- `task format` — `uvx ruff format` then `uvx ruff check --fix`
- `task validate-workflows` — `uvx zizmor` on `.github/workflows`
- `task pr` — runs check + format + test + validate-workflows (use before opening a PR)
- `task add-package -- <name>` — add a dependency from PyPI

To run Python directly, use `uv run <command>` (or activate `.venv`).

## Conventions

Code style specified in pyproject.toml via Ruff.

### Settings & environment variables

- All configuration goes through `src/settings.py` (`AppSettings` / `settings`), backed by
  `pydantic-settings`. Add new env-driven config as fields on `AppSettings` (use `SecretStr`
  for secrets) and document them in `.env.example`.
- `.env` is auto-loaded by Taskfile, the VSCode Python extension, and `AppSettings` itself
  (via `pydantic-settings` `env_file=".env"`). It is not loaded into arbitrary shells, so
  for ad-hoc commands run through `task` / `uv run`, or source `.env` explicitly.

### Logging

- Call `setup_logging()` once from the entry point; obtain loggers via
  `logging.getLogger(__name__)`.
- The log level comes from `settings.log_level` unless explicitly overridden.

### Tests

- Live in `tests/` at the repo root; import from `src.*`.

### Dependencies

- Runtime deps go under `[project].dependencies`; dev deps under
  `[dependency-groups].dev`.
- Use `uv add <pkg>` for public PyPI packages.
- Use `task add-package -- <pkg>` for runtime dependencies.

### GitHub Actions

- PR validation uses the local workflow in `.github/workflows/pr-checks.yml`.
- All third-party actions are pinned to a commit SHA with a version comment (required by zizmor).
