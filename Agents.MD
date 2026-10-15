# Project agents guide

This repository is a full-stack boilerplate: **FastAPI** backend and **React (TypeScript)** frontend.

## Layout

- `backend/` — API with layered architecture (`types`, `models`, `repositories`, `services`, `routers`, `utils`). Data is stored in JSON files under `backend/data/` (one file per entity, contents are a JSON array). Uses **uv**, **Pydantic**, and FastAPI dependency injection (routers depend on services; services use repositories).
- `frontend/` — **React + TypeScript**, **shadcn/ui**, **Redux Toolkit** (RTK Query for API, slices for UI state).
- `docs/` — Consolidated feature documentation with one folder per feature (`docs/<feature>/`) covering business requirements, architecture, and test cases across full-stack.

## Current scope

**Personal Budget Planner** — Web application for managing personal income, expenses, categories, monthly budgets, financial history, analytics, and user authentication.

## Working conventions

- Add new features under the same layer folders on the backend and under `src/features/` on the frontend.
- Document each feature under `docs/<feature>/` (consolidated for full-stack: business requirements, architecture, test cases).
- Keep AI assistant entry points minimal: this file is the source of truth; `Claude.md` points here.

## Local development

### One-Click Startup (Windows)
Run `start.bat` from the root directory. It automatically checks Node and uv/Python prerequisites, installs backend and frontend dependencies, launches both development servers in separate windows, and opens the application in your browser (`http://localhost:5174`).

### Manual Startup & Verification
1. Backend: from `backend/`:
   - Run server: `uv sync` then `uv run uvicorn app.main:app --reload --port 8001`.
   - Format: `uv run ruff format .` (verify with `uv run ruff format --check .`).
   - Lint: `uv run ruff check .` (auto-fix with `uv run ruff check --fix .`).
   - Type check: `uv run mypy app`.
   - Automated tests: `uv run pytest`.
2. Frontend: from `frontend/`:
   - Run dev server: `npm install` then `npm run dev` (dev server port **5174**; default API base: `http://localhost:8001/api`).
   - Format: `npm run format` (verify with `npm run format:check`).
   - Lint: `npm run lint`.
   - Type check: `npm run typecheck`.
   - Build: `npm run build`.

VS Code: `.vscode/launch.json` starts the backend; `.vscode/tasks.json` installs dependencies and runs the frontend dev server.

## Agent Customizations (Rules, Skills, Hooks)
- **Path Filters (Globs)**:
  - Backend path filter (`backend/**/*`): automatically applies backend rules, skills, and quality hooks.
  - Frontend path filter (`frontend/**/*`): automatically applies frontend rules, skills, and quality hooks.
- **Rules**:
  - Backend Rules (Path Filter: `backend/**/*`):
    - [`.agents/rules/backend/architecture-and-layering.md`](./.agents/rules/backend/architecture-and-layering.md) — 5-layer architecture, Pydantic v2, data store covariance.
    - [`.agents/rules/backend/security-and-multitenancy.md`](./.agents/rules/backend/security-and-multitenancy.md) — JWT auth, user isolation, data scoping.
    - [`.agents/rules/backend/code-quality-and-testing.md`](./.agents/rules/backend/code-quality-and-testing.md) — Ruff, Mypy, Pytest isolated fixtures.
    - [`backend/AGENTS.md`](./backend/AGENTS.md) — Local backend rules summary.
  - Frontend Rules (Path Filter: `frontend/**/*`):
    - [`.agents/rules/frontend/architecture-and-components.md`](./.agents/rules/frontend/architecture-and-components.md) — Feature-first layout, shadcn/ui, TypeScript.
    - [`.agents/rules/frontend/state-and-rtk-query.md`](./.agents/rules/frontend/state-and-rtk-query.md) — RTK Query cache tags, mutations, Redux slices.
    - [`.agents/rules/frontend/code-quality-and-formatting.md`](./.agents/rules/frontend/code-quality-and-formatting.md) — Prettier, Oxlint, strict typecheck.
    - [`frontend/AGENTS.md`](./frontend/AGENTS.md) — Local frontend rules summary.
  - Editor Rules & MDC:
    - [`.cursorrules`](./.cursorrules) — Integrated rule-set with path filters for Cursor.
    - [`.cursor/rules/backend.mdc`](./.cursor/rules/backend.mdc) — Backend rule with glob filter `backend/**/*`.
    - [`.cursor/rules/frontend.mdc`](./.cursor/rules/frontend.mdc) — Frontend rule with glob filter `frontend/**/*`.
- **Skills**:
  - Backend (`backend/**/*`): [`.agents/skills/backend-development/SKILL.md`](./.agents/skills/backend-development/SKILL.md)
  - Frontend (`frontend/**/*`): [`.agents/skills/frontend-development/SKILL.md`](./.agents/skills/frontend-development/SKILL.md)
- **Hooks**:
  - Configuration: [`.agents/hooks.json`](./.agents/hooks.json) — Safety guards, `path_filters`, and linting/typechecking verification.
