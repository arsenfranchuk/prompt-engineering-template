# Claude Agent Guide: Personal Budget Planner

Welcome to the **Personal Budget Planner** project. This document serves as the primary guidance for AI coding assistants and developers. It outlines stack details, architecture, execution commands, code quality workflows, and critical rules.

---

## 1. Project Overview & Architecture

Full-stack web application designed for personal finance management: income, expenses, categories, monthly budgets, analytics, and user authentication.

### Technology Stack
- **Backend**: Python 3.12, **FastAPI**, **Pydantic v2**, **uv** package manager.
- **Frontend**: **React 19**, **TypeScript**, **Vite**, **Tailwind CSS v4**, **shadcn/ui**, **Redux Toolkit** (RTK Query + UI slices).
- **Data Store**: Persistent JSON storage under `backend/data/<entity>.json` accessed through a layered repository pattern.

### Layered Architecture

#### Backend (`backend/`)
- `app/models/` — Pydantic models for validation (`*Create`, `*Update`, `*InDb`, `*Response`).
- `app/repositories/` — Encapsulates storage read/write via `app.utils.json_store`. Filters all queries by authenticated `user_id`.
- `app/services/` — Business logic, financial rules, cross-entity constraints, error raising.
- `app/routers/` — FastAPI endpoint definitions, status codes, route parameters, dependency injection.
- `app/types/` — Type aliases and NewType identifiers (`UserId`, `CategoryId`, etc.).
- `app/utils/` — Store helpers (`json_store`), password hashing, JWT authentication.
- `tests/` — Automated Pytest suite. Storage isolation is handled via `tests/conftest.py`.

#### Frontend (`frontend/`)
- `src/features/<feature>/` — Feature-first layout (`auth/`, `budgets/`, `categories/`, `dashboard/`, `profile/`, `statistics/`, `transactions/`).
- `src/components/ui/` — Reusable primitive UI components (`Button`, `Card`, `Dialog`, etc.).
- `src/components/` — Shared structural layouts (`AppLayout.tsx`).
- `src/store/api/` — RTK Query services with tag-based cache invalidation.
- `src/store/slices/` — Redux slices for client-side state.
- `src/types/` — Strict TypeScript types and interfaces matching backend schemas.

---

## 2. Command Reference

### Local Development
```bash
# Automated Start (Windows root)
start.bat

# Backend (from backend/)
uv sync
uv run uvicorn app.main:app --reload --port 8001

# Frontend (from frontend/)
npm install
npm run dev -- --port 5174
```

### Code Quality, Linting & Formatting

#### Backend (`backend/`)
```bash
# Formatter (Ruff)
uv run ruff format .
uv run ruff format --check .

# Linter (Ruff)
uv run ruff check .
uv run ruff check --fix .

# Type Checker (Mypy)
uv run mypy app

# Tests (Pytest)
uv run pytest
```

#### Frontend (`frontend/`)
```bash
# Formatter (Prettier)
npm run format
npm run format:check

# Linter (Oxlint)
npm run lint

# Type Checker (TypeScript)
npm run typecheck

# Production Build
npm run build
```

---

## 3. Core Working Conventions & Rules

1. **Multi-Tenancy & Data Isolation**:
   - Every entity record must contain a valid `user_id`.
   - Never extract `user_id` from client payloads. Always derive the identity from the authenticated JWT session via `get_current_user`.
   - Queries must always filter by `user_id`.

2. **Strict Layering**:
   - Routers depend exclusively on Services.
   - Services depend exclusively on Repositories and models.
   - Repositories encapsulate JSON store interactions. Never execute raw file operations inside routers or services.

3. **Financial Computations & Safeguards**:
   - Monetary amounts must strictly be positive numbers (`amount > 0`).
   - Round financial amounts to 2 decimal places.
   - Categories referenced by active transactions or budgets must NOT be deleted.
   - Destructive actions in the UI must require user confirmation dialogs.

4. **Verification Requirement**:
   - Before completing tasks, always run formatting, linting, typechecking, and tests on the modified project parts.

---

## 4. Agent Customization Links
- Root Guide: [Agents.MD](./Agents.MD)
- Dedicated Rules:
  - Backend Rules (Path Filter: `backend/**/*`):
    - [.agents/rules/backend/architecture-and-layering.md](./.agents/rules/backend/architecture-and-layering.md)
    - [.agents/rules/backend/security-and-multitenancy.md](./.agents/rules/backend/security-and-multitenancy.md)
    - [.agents/rules/backend/code-quality-and-testing.md](./.agents/rules/backend/code-quality-and-testing.md)
    - [backend/AGENTS.md](./backend/AGENTS.md)
  - Frontend Rules (Path Filter: `frontend/**/*`):
    - [.agents/rules/frontend/architecture-and-components.md](./.agents/rules/frontend/architecture-and-components.md)
    - [.agents/rules/frontend/state-and-rtk-query.md](./.agents/rules/frontend/state-and-rtk-query.md)
    - [.agents/rules/frontend/code-quality-and-formatting.md](./.agents/rules/frontend/code-quality-and-formatting.md)
    - [frontend/AGENTS.md](./frontend/AGENTS.md)
  - Editor Rules & MDC:
    - Cursor Rules: [.cursorrules](./.cursorrules)
    - Backend MDC: [.cursor/rules/backend.mdc](./.cursor/rules/backend.mdc) (glob: `backend/**/*`)
    - Frontend MDC: [.cursor/rules/frontend.mdc](./.cursor/rules/frontend.mdc) (glob: `frontend/**/*`)
- Dedicated Skills:
  - Backend Skill (`backend/**/*`): [.agents/skills/backend-development/SKILL.md](./.agents/skills/backend-development/SKILL.md)
  - Frontend Skill (`frontend/**/*`): [.agents/skills/frontend-development/SKILL.md](./.agents/skills/frontend-development/SKILL.md)
- Quality Hooks: [.agents/hooks.json](./.agents/hooks.json) (configured with `path_filters`)
