# Python Template Repository

This is a template repository for Python projects. It provides a standardized structure,
configurations, and tools to help getting started quickly and keep consistency across projects.

## Project structure

```text
.
├── .devcontainer/                   # Dev container configuration
│   ├── Dockerfile                   # Container image definition
│   └── devcontainer.json            # VSCode dev container settings and extensions
├── .github/
│   ├── workflows/
│   │   └── pr-checks.yml            # CI checks run on pull requests
│   └── dependabot.yml               # Dependabot configuration for dependency updates
├── .vscode/
│   ├── launch.json                  # Debugger launch configurations
│   └── settings.json                # VSCode workspace settings
├── src/                             # Application source code
│   ├── logging_config.py            # Logging setup utilities
│   └── settings.py                  # App settings loaded from environment variables
├── tests/                           # Test code
├── .env.example                     # Template for required environment variables
├── main.py                          # Entry point
├── pyproject.toml                   # Project metadata and dependencies
├── uv.lock                          # Locked dependency versions (managed by uv)
├── README.md
└── Taskfile.yml                     # Task runner commands
```

## Setup instructions

Below are two methods to set up the development environment, with a Visual Studio Code devcontainer
or manually.

### Devcontainer

This repository has [configurations for a devcontainer](.devcontainer).
To set up the development environment:

- Copy `.env.example` to `.env` and fill in the required values:

  ```bash
  cp .env.example .env
  ```

- Install and start a Docker daemon, usually Docker Desktop.
- Install Visual Studio Code (VSCode).
- Install Dev Container extension in VSCode.
- In VSCode Run the command `Dev Containers: Rebuild and Reopen in Container` from the
  Command Palette (Ctrl+Shift+P) or accept the prompt to reopen in the container which
  should appear when you open the repository.
- Wait for the container to build and open. The development environment is now ready to use.

If you want to go back to your local environment, you can run the command
`Dev Containers: Reopen Folder Locally` from the Command Palette.

### Manual setup

- Copy `.env.example` to `.env` and fill in the required values:
- Install [uv](https://docs.astral.sh/uv/getting-started/installation/) for Python and dependency management
- Install [Task](https://taskfile.dev/installation/) command runner
- Install python dependencies: `task install`
- (Optional) Install VSCode extensions. The most important is the Python extension. See the
  [devcontainer.json](.devcontainer/devcontainer.json) file for a full list of recommended
  extensions.

## Development

This project is configured with Taskfile, uv, Pytest, Ruff, ty, VSCode settings,
and devcontainer.

### Running Python

To run Python commands from the terminal you either need to use `uv run <command>` or activate
the virtual environment.

### Running commands

This project uses Task which replaces traditional tools like Make to simplify and standardize
running commands.
Commands are defined in `Taskfile.yml` file which can be read directly to understand how it works.
Task lets you run commands with:

```bash
task <command>
```

There are predefined helper commands to streamline common tasks such as running code, tests,
linting, and formatting. You can view the full list of available commands by running:

```bash
task --list
```

### Available tasks

| Command                     | Description                                                 |
| --------------------------- | ----------------------------------------------------------- |
| `task install`              | Install all dependencies                                    |
| `task run`                  | Run the main application                                    |
| `task check`                | Run type checker (ty)                                       |
| `task format`               | Format and lint with auto-fix                               |
| `task test`                 | Run tests with pytest                                       |
| `task validate-workflows`   | Scan GitHub workflows with zizmor                           |
| `task pr`                   | Run all checks (check → format → test → validate-workflows) |
| `task add-package`          | Add a package from PyPI                                     |

### Dependabot

This project uses [Dependabot](.github/dependabot.yml) to keep Python and GitHub Actions
dependencies up to date with weekly pull requests.

### Environment variables

Variables are defined in `.env` (copied from `.env.example`) and auto-loaded in three places:

- The VSCode Python extension, into new VSCode-managed terminals (not external shells,
  tmux panes, or AI coding agent shells).
- The Task runner via `dotenv: [.env]` in `Taskfile.yml`.
- `AppSettings` in `src/settings.py`, via `pydantic-settings` `env_file=".env"`.

For other shells, run commands through `task` / `uv run`, or source `.env` manually.

## Python package layout

For Python code that are not intended to be used as a library by other projects,
we use a simple package layout where all code is contained within a single folder named `src`.

Technically, this is called a
["flat layout"](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
where the package is named `src`.
This should not be confused with the
["src layout"](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
where src folder contains one folder with the package name.
