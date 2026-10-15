---
description: React frontend code quality, Prettier formatting, Oxlint linting, and typecheck rules.
trigger: glob
globs: "frontend/**/*"
---

# Frontend Code Quality & Formatting Rules

These rules govern formatting, linting, typechecking, and production build verification for the frontend.

## 1. Zero-Defect Policy
- Frontend changes must pass all quality tools with **0 errors and 0 warnings** before task completion.
- Do not disable linting rules or use `@ts-ignore` without explicit justification.

## 2. Tooling & Execution Commands
From the `frontend/` directory:

1. **Linter (Oxlint)**:
   ```bash
   npm run lint
   ```
2. **Formatter (Prettier)**:
   ```bash
   npm run format
   # To verify without altering files:
   npm run format:check
   ```
3. **Type Checker (TypeScript)**:
   ```bash
   npm run typecheck
   # (Equivalent to npx tsc --noEmit)
   ```
4. **Production Build**:
   ```bash
   npm run build
   # (Runs tsc -b and vite build)
   ```

## 3. Formatting Standards
- Semicolons: enabled (`true`).
- Single quotes: enabled (`true`).
- Tab width: 2 spaces.
- Print width: 100 characters.
- Trailing commas: `es5`.
