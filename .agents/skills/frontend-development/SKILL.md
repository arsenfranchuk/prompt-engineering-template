---
name: frontend-development
description: Expert instructions and workflows for React, TypeScript, Vite, Tailwind CSS, and Redux Toolkit frontend development in the Personal Budget Planner project.
trigger: glob
globs: "frontend/**/*"
---

# Frontend Development Skill

## Overview
This skill guides the development and maintenance of the React frontend in `frontend/`. The stack consists of **React 19**, **TypeScript**, **Vite**, **Tailwind CSS v4**, **shadcn/ui** components, and **Redux Toolkit** (RTK Query for API integration, client slices for local UI state).

## Directory Structure & Feature-First Pattern
```
frontend/
├── src/
│   ├── components/         # Shared UI components
│   │   ├── ui/             # shadcn/ui primitives (button, card, dialog, input, label, textarea)
│   │   └── AppLayout.tsx   # Responsive app shell with desktop/mobile navigation
│   ├── features/           # Feature modules (feature-first architecture)
│   │   ├── auth/           # Login, Register, ProtectedRoute
│   │   ├── budgets/        # Budget lists, progress bars, create/edit dialogs
│   │   ├── categories/     # Category listing, color/icon, creation/deletion
│   │   ├── dashboard/      # Financial overview cards, recent activity, metrics
│   │   ├── profile/        # User profile, password update
│   │   ├── statistics/     # Breakdown charts, monthly comparisons
│   │   └── transactions/   # Transaction list, filter/sort, create/edit modal
│   ├── lib/                # Utilities (`cn` helper, config, API base URL)
│   ├── store/              # Redux Toolkit store configuration
│   │   ├── api/            # RTK Query API slices with cache tags
│   │   ├── slices/         # UI & client state slices (e.g. authSlice)
│   │   ├── hooks.ts        # Typed hooks: `useAppDispatch`, `useAppSelector`
│   │   └── store.ts        # Root store configuration
│   ├── types/              # TypeScript interface definitions matching backend models
│   ├── App.tsx             # Root router definitions
│   └── main.tsx            # Entry point with Provider & BrowserRouter
├── .oxlintrc.json          # Oxlint configuration
├── .prettierrc             # Prettier formatting rules
└── package.json            # Scripts & dependencies
```

## Mandatory Development Rules
1. **Feature Encapsulation**:
   - Feature pages, feature-specific dialogs, and helper components must live in `src/features/<feature>/`.
   - Shared layout wrappers belong in `src/components/`, while reusable design-system controls belong in `src/components/ui/`.
2. **RTK Query Conventions**:
   - Use tag types (`'Transactions'`, `'Budgets'`, `'Categories'`, `'Dashboard'`, `'User'`) for automatic cache invalidation upon mutation.
   - Always handle `isLoading`, `isFetching`, and `error` states gracefully with loaders and error messages.
3. **Type Safety**:
   - Never use `any`. Always define strict interfaces in `src/types/<feature>.ts`.
   - Ensure backend response formats match frontend types.
4. **UX & Design System**:
   - Follow semantic colors:
     - **Green** (e.g. `text-emerald-600`, `bg-emerald-50`): Income, positive net balance, on-budget status.
     - **Red / Destructive** (e.g. `text-red-600`, `bg-red-50`): Expenses, exceeded budgets, deletion actions.
     - **Amber / Yellow**: Warning state (e.g. budget > 80% used).
   - Confirmation dialogs are mandatory before destructive actions (deleting categories, transactions, or budgets).
   - Responsive layouts: Support mobile screens (hamburger drawer) and desktop screens (fixed sidebar).

## Verification Commands
Before completing frontend tasks, execute the following checks from the `frontend/` directory:

```bash
# 1. Format code with Prettier
npm run format

# 2. Verify formatting compliance
npm run format:check

# 3. Lint code with Oxlint
npm run lint

# 4. Strict TypeScript type check
npm run typecheck

# 5. Build verification
npm run build
```
