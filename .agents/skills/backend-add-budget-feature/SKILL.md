---
name: backend-add-budget-feature
description: Step-by-step workflow for adding a new backend feature following the 5-layer FastAPI architecture in Personal Budget Planner.
trigger: glob
globs: "backend/**/*"
---

# Backend Add Feature Skill

## Workflow
When implementing a new feature in `backend/`, follow this strict bottom-up order:

1. **Types (`app/types/`)**:
   - Define type aliases and strong NewType identifiers if needed (e.g. `BudgetId`, `CategoryId`).
2. **Models (`app/models/`)**:
   - Create Pydantic v2 schemas: `*Base`, `*Create`, `*Update`, `*InDb`, `*Response`.
3. **Repository (`app/repositories/`)**:
   - Implement storage persistence with `user_id` filtering. Use `Sequence[BaseModel]` in write methods.
4. **Service (`app/services/`)**:
   - Implement domain business logic, input validation, and positive financial computations.
5. **Router (`app/routers/`)**:
   - Declare FastAPI endpoints using dependency injection (`Depends(get_service)`).
6. **Documentation & Tests**:
   - Add feature documentation under `docs/<feature>/` and write isolated Pytest tests under `backend/tests/`.
