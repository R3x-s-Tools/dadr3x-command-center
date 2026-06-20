# CI Setup

This project uses GitHub Actions for the first quality gate.

## What CI checks

- Ruff lint
- Black formatting
- Pytest unit tests
- Coverage report in terminal

## Local commands

Install dev dependencies:

```bash
pip install -r requirements-dev.txt
```

Run everything locally:

```bash
ruff check .
black --check .
pytest --cov=analytics --cov=ai --cov=core --cov=reports --cov=services --cov-report=term-missing
```

Auto-format:

```bash
black .
ruff check . --fix
```

## Branch protection

After the workflow runs once on GitHub, go to:

Settings → Branches → main → Branch protection

Enable:

- Require a pull request before merging
- Require branches to be up to date before merging
- Require status checks to pass before merging

Select this required check:

```text
Tests / Lint / Format
```
