---
name: backend-development
description: Expert instructions and workflows for FastAPI backend development, testing, linting, formatting, and type checking in the Personal Budget Planner project.
trigger: glob
globs: "backend/**/*"
---

# Backend Development Skill

## Overview
This skill guides the development and maintenance of the FastAPI backend in `backend/`. The backend uses Python 3.12, **uv** for dependency management, Pydantic v2 for data validation, and JSON array file-based storage under `backend/data/`.

## Architectural Layers
All features must strictly follow the layered architecture:
```
backend/
├── app/
│   ├── models/         # Pydantic v2 schemas (Create, Update, InDb, Response)
│   ├── repositories/   # JSON persistence via JsonStore, filtered by user_id
│   ├── services/       # Core business logic, mathematical calculations, validations
│   ├── routers/        # FastAPI HTTP endpoints, status codes, dependency injection
│   ├── types/          # Type aliases, NewType IDs (UserId, CategoryId, etc.)
│   ├── utils/          # json_store, security (hashing, JWT tokens)
│   ├── dependencies.py # FastAPI dependency providers (repositories, services, current_user)
│   └── main.py         # App factory, CORS, exception handlers, router mounts
├── data/               # Persistent JSON files (e.g. users.json, transactions.json)
├── tests/              # Pytest test suite with isolated_storage fixture
└── pyproject.toml      # uv configuration, ruff, mypy, pytest settings
```

## Mandatory Development Rules
1. **Multi-Tenancy & Data Isolation**:
   - Every entity must link to `user_id`.
   - Never accept `user_id` blindly from request bodies; extract it from the authenticated session (`get_current_user`).
   - All repository read/write/delete operations must strictly filter by the authenticated user's ID.
2. **Layering Integrity**:
   - Routers only call Services via FastAPI `Depends()`.
   - Services only call Repositories and models. Never import routers or write raw file I/O in services.
   - Repositories encapsulate all data access through `app.utils.json_store`. Use `Sequence[BaseModel]` for write operations.
3. **Financial Computations**:
   - All monetary amounts must be strictly positive (`amount > 0`).
   - Round values to 2 decimal places (`round(amount, 2)`).
   - Category deletion must be protected: never delete categories referenced by active transactions or budgets.

## Verification Commands
Always run the complete verification suite after making changes:

```bash
# 1. Format code (Ruff)
uv run ruff format .

# 2. Check formatting
uv run ruff format --check .

# 3. Lint code (Ruff)
uv run ruff check .

# 4. Auto-fix linting issues where possible
uv run ruff check --fix .

# 5. Static type check (Mypy)
uv run mypy app

# 6. Run automated test suite (Pytest)
uv run pytest
```

## Adding a New Backend Feature
1. **Define Models** in `app/models/<entity>.py`:
   - `<Entity>Base`, `<Entity>Create`, `<Entity>Update`, `<Entity>InDb`, `<Entity>Response`.
2. **Define Repository** in `app/repositories/<entity>_repository.py`:
   - Methods: `list_by_user(user_id)`, `get_by_id(id)`, `create(item)`, `update(item)`, `delete(id)`.
3. **Define Service** in `app/services/<entity>_service.py`:
   - Implement business logic, ownership checks, raise domain exceptions (e.g., `<Entity>NotFoundError`).
4. **Register Dependencies** in `app/dependencies.py`:
   - Add factory functions `get_<entity>_repository` and `get_<entity>_service`.
5. **Implement Router** in `app/routers/<entity>s.py`:
   - Expose endpoints with status codes, Pydantic response models, and user dependency.
6. **Mount Router** in `app/main.py`.
7. **Write Tests** in `tests/test_<entity>.py`:
   - Ensure tests use `tmp_path` (handled automatically via `tests/conftest.py` fixture).
