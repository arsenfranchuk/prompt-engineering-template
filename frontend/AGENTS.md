# Frontend Rules & Guidelines (React + TypeScript)

## 1. Architecture & Directory Organization

- **Feature-First Structure** (`src/features/<feature>/`):
  - Place all page components, feature-specific dialogs, and subcomponents inside their designated feature folder (e.g., `auth/`, `budgets/`, `categories/`, `dashboard/`, `profile/`, `statistics/`, `transactions/`).
- **Shared Components** (`src/components/`):
  - Generic UI primitives belong in `src/components/ui/` (shadcn/ui style).
  - Shared layout templates (e.g., `AppLayout.tsx`) belong in `src/components/`.
- **Global State & API** (`src/store/`):
  - API queries, mutations, and caching live in `src/store/api/` using RTK Query.
  - Client state slices live in `src/store/slices/`.
  - Use custom typed hooks `useAppDispatch` and `useAppSelector` from `src/store/hooks.ts`.

## 2. RTK Query & Cache Invalidation

- Define tag types in API slices (e.g., `'Transactions'`, `'Budgets'`, `'Categories'`, `'Dashboard'`).
- Ensure mutation endpoints invalidate relevant tags so the UI automatically updates without manual re-fetching.
- Handle `isLoading`, `isFetching`, and `error` states gracefully on all screens.

## 3. UI/UX & Styling Standards

- Use **Tailwind CSS** utility classes and semantic styling.
- Component styling should remain consistent with **shadcn/ui** patterns.
- Clear visual distinction:
  - Green for positive balance and income.
  - Red / destructive for expenses and exceeded budgets.
  - Amber / yellow for warning states (approaching budget limits).
- Every interactive action with potential data loss (e.g., deleting a category, transaction, or budget) must use a confirmation modal.
- Always provide responsive layouts that adapt cleanly from mobile to desktop.

## 4. Code Quality & Verification

- Strict TypeScript: Avoid `any`. All API models must have matching interfaces in `src/types/`.
- Run quality checks before completing tasks:
  - Format: `npm run format` (check with `npm run format:check` via Prettier)
  - Lint: `npm run lint` (using oxlint)
  - Typecheck: `npm run typecheck` (or `npx tsc --noEmit`)
  - Build: `npm run build`
