---
description: FastAPI backend code quality, Ruff linting/formatting, Mypy typing, and isolated Pytest testing rules.
trigger: glob
globs: "backend/**/*"
---

# Backend Coding Standards & Testing Rules

These rules govern linting, formatting, type checking, and automated test enforcement on the FastAPI backend.

## 1. Zero-Defect Policy
- Backend changes must pass all quality tools with **0 errors and 0 warnings** before task completion.

## 2. Tooling & Execution Commands
From the `backend/` directory:

1. **Linter (Ruff)**:
   ```bash
   uv run ruff check .
   uv run ruff check --fix .
   ```
2. **Formatter (Ruff)**:
   ```bash
   uv run ruff format .
   uv run ruff format --check .
   ```
3. **Type Checker (Mypy)**:
   ```bash
   uv run mypy app
   ```
4. **Automated Tests (Pytest)**:
   ```bash
   uv run pytest
   ```

## 3. Test Isolation & Storage Invariants
- Tests must live under `backend/tests/`.
- Every test must use isolated temporary storage provided by the `isolated_storage` fixture in `backend/tests/conftest.py`.
- **Prohibited**: Writing to or reading from `backend/data/*.json` during test runs. The files in `backend/data/` must always remain empty JSON arrays (`[]`) when clean.
- **Dynamic Dates**: Do not hardcode specific calendar months in tests. Always generate test dates dynamically using `datetime.now(timezone.utc)`.
