---
name: frontend-run-budget
description: Instructions for installing dependencies and launching the React Vite development server for Personal Budget Planner.
trigger: glob
globs: "frontend/**/*"
---

# Frontend Run Skill

## Startup Workflow

1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. Access the web interface:
   - Local App URL: `http://localhost:5174`
   - Default backend API proxy: `http://localhost:8001/api`
