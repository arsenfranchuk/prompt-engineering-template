---
name: backend-run-budget
description: Instructions for synchronizing dependencies and running the FastAPI backend server for Personal Budget Planner.
trigger: glob
globs: "backend/**/*"
---

# Backend Run Skill

## Startup Workflow

1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Synchronize environment and dependencies with `uv`:
   ```bash
   uv sync
   ```
3. Start the FastAPI development server with hot-reload on port 8001:
   ```bash
   uv run uvicorn app.main:app --reload --port 8001
   ```
4. Verify the API status:
   - Interactive Swagger Docs: `http://localhost:8001/docs`
   - Healthcheck: `http://localhost:8001/api/health`
