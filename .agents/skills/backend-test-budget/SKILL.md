---
name: backend-test-budget
description: Verification workflows for the FastAPI backend including Ruff format/lint, Mypy typechecking, and isolated Pytest suite.
trigger: glob
globs: "backend/**/*"
---

# Backend Test & Quality Skill

## Full Verification Suite

Execute all verification steps from the `backend/` directory:

```bash
# 1. Format verification (Ruff)
uv run ruff format --check .

# 2. Linting verification (Ruff)
uv run ruff check .

# 3. Static type checking (Mypy)
uv run mypy app

# 4. Automated tests (Pytest with isolated storage)
uv run pytest
```

## Auto-Fixes
To automatically resolve formatting or linting warnings:
```bash
uv run ruff format .
uv run ruff check --fix .
```
