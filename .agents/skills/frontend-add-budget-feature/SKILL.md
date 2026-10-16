---
name: frontend-add-budget-feature
description: Step-by-step workflow for implementing a new frontend feature using feature-first structure, shadcn/ui, and RTK Query in Personal Budget Planner.
trigger: glob
globs: "frontend/**/*"
---

# Frontend Add Feature Skill

## Workflow
When developing a new user-facing feature in `frontend/`, follow this structure:

1. **Feature Directory (`src/features/<feature>/`)**:
   - Create a dedicated folder for the feature containing components, hooks, and views.
2. **Types (`src/types/`)**:
   - Define TypeScript interfaces matching backend Pydantic models.
3. **RTK Query API Slice (`src/store/api/`)**:
   - Add query and mutation endpoints with appropriate `providesTags` and `invalidatesTags`.
4. **UI Components**:
   - Use Tailwind CSS and shadcn/ui primitives from `src/components/ui/`.
   - Implement loading spinners (`isLoading`) and user-friendly error banners (`isError`).
5. **Route Registration**:
   - Mount new views into `src/App.tsx` or router configuration with protected layout wrappers.
