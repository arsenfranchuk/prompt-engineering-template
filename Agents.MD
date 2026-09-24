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

### Manual Startup
1. Backend: from `backend/`, run `uv sync` then `uv run uvicorn app.main:app --reload --port 8001`.
2. Frontend: from `frontend/`, run `npm install` then `npm run dev` (dev server port **5174**; default API base: `http://localhost:8001/api`).
3. Automated Tests: from `backend/`, run `uv run pytest`.

VS Code: `.vscode/launch.json` starts the backend; `.vscode/tasks.json` installs dependencies and runs the frontend dev server.
