# Refactoring Coder

Refactoring Coder is a small Python command-line sample for exploring
Anthropic's Python SDK and Claude tool use. It asks a Claude model to create
characterization tests for a deliberately verbose URL slug function, then
refactor that function while preserving behavior.

> [!WARNING]
> This is an experimental project and should not be considered production-ready.

The project is intentionally small so the agent workflow stays visible. The
agent is not given direct file-system or command-line access. Instead, it can
only call narrow Python tools that read and save specific files, plus a tool
that runs the project check script.

## What It Does

The repository contains two console applications:

- `url_slug_maker`: a simple CLI that converts input text into a URL slug.
- `refactoring_coder`: a Claude-backed agent that works on the slug maker code.

The slug maker can be run directly:

```powershell
.\.venv\Scripts\python.exe -m url_slug_maker This is the season's "new thing".
```

Example output:

```text
URL slug: this-is-the-seasons-new-thing
```

The refactoring agent flow is:

1. Read the current `src/url_slug_maker/utilities.py` file.
2. Read the current `tests/test_utilities.py` file.
3. Create characterization tests for the current `create_url_slug` behavior.
4. Save the updated unit test file.
5. Run the project checks.
6. Refactor the slug-making implementation to reduce cognitive complexity.
7. Save the updated code file.
8. Run the project checks again.
9. Continue making small corrections until the checks pass.

## Requirements

- Python 3.11.
- PowerShell on Windows.
- An `ANTHROPIC_API_KEY` environment variable for Claude model calls.

## Setup

Create the virtual environment and install the project with development
dependencies:

```powershell
.\scripts\setup-dev.ps1
```

The setup script expects Python 3.11 at the path configured in
`scripts\setup-dev.ps1`.

## Running

Run the URL slug maker from the repository root:

```powershell
.\.venv\Scripts\python.exe -m url_slug_maker This is the season's "new thing".
```

Run the refactoring agent from the repository root:

```powershell
.\.venv\Scripts\python.exe -m refactoring_coder
```

The refactoring agent reads and updates only the files exposed by its local
tools.

## Development Checks

Run formatting, linting, type checking, and tests:

```powershell
.\scripts\check.ps1
```

This runs:

- `ruff format .`
- `ruff check .`
- `pyright`
- `pytest`

## Project Structure

```text
src/refactoring_coder/
  __main__.py  Package entry point for python -m refactoring_coder
  cli.py       Command-line entry point for the refactoring agent
  agent.py     Claude message loop, tool schemas, and refactoring workflow
  tools.py     Narrow local tools exposed to the agent

src/url_slug_maker/
  __main__.py  Package entry point for python -m url_slug_maker
  cli.py       Command-line entry point for slug generation
  utilities.py Slug generation function used as the refactoring target

tests/
  test_smoke.py
  test_utilities.py

scripts/
  setup-dev.ps1
  check.ps1
```

## Notes

This project is an agent learning exercise, not a general-purpose coding agent.
The tool layer is deliberately constrained so the model can only inspect and
update the specific source and test files used by the exercise.

Agent behavior and final wording can vary between runs because the refactoring
workflow is model-driven. Anthropic API calls may incur usage costs.

## Third-Party Notices

This project has a direct runtime dependency on the `anthropic` Python package.
See the package's PyPI license metadata for full license and notice terms.

## License

GNU General Public License v3.0. See the `LICENSE` file for details.
