---
description: React frontend RTK Query API slices, tag cache invalidation, and Redux client state rules.
trigger: glob
globs: "frontend/**/*"
---

# Frontend State Management & RTK Query Rules

These rules govern remote API caching, local UI state, and mutations on the React frontend.

## 1. Remote Server State (RTK Query)
- All network requests to the backend must be made through RTK Query API slices under `src/store/api/`.
- Configure explicit `tagTypes`:
  - `'Auth'`: User session and profile.
  - `'Transactions'`: Financial transaction records.
  - `'Budgets'`: Budget allocations and progress metrics.
  - `'Categories'`: Income and expense category definitions.
  - `'Dashboard'`: Summary financial balances and analytics.
- Mutations must declare `invalidatesTags` so that related queries re-fetch automatically upon data updates.
- All views must handle `isLoading`, `isFetching`, and `error` states gracefully with loaders and error messages.

## 2. Client UI State (Redux Slices)
- Client-only state (e.g., auth tokens in local memory, active filters, UI preferences) lives in `src/store/slices/`.
- Always use the typed custom hooks from `src/store/hooks.ts`:
  - `useAppDispatch()`
  - `useAppSelector()`
- Do not import `useDispatch` or `useSelector` directly from `react-redux` in components.
