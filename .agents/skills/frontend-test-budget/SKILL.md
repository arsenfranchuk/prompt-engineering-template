---
name: frontend-test-budget
description: Verification workflows for the React frontend including Oxlint linting, Prettier formatting, TypeScript typecheck, and Vite production build.
trigger: glob
globs: "frontend/**/*"
---

# Frontend Test & Quality Skill

## Full Verification Suite

Execute all verification steps from the `frontend/` directory:

```bash
# 1. Lint verification (Oxlint)
npm run lint

# 2. Format verification (Prettier)
npm run format:check

# 3. Type checking (TypeScript)
npm run typecheck

# 4. Production build verification
npm run build
```

## Auto-Formatting
To auto-format all frontend files according to project style:
```bash
npm run format
```
