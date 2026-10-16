---
description: React frontend feature-first directory layout, shadcn/ui components, and TypeScript standards.
trigger: glob
globs: "frontend/**/*"
---

# Frontend Architecture Rules

These rules govern directory organization, component design, and styling on the React frontend.

## 1. Feature-First Directory Structure
All feature-specific code must reside within `src/features/<feature>/`:
- `auth/`: Authentication views, login/registration forms, protected route guards.
- `budgets/`: Budget lists, category tracking, budget create/edit dialogs.
- `categories/`: Category listings, icon/color selectors, category dialogs.
- `dashboard/`: Overview metric cards, summary statistics, recent activity.
- `profile/`: User profile details, password change forms.
- `statistics/`: Visual breakdown charts, category share, period comparisons.
- `transactions/`: Transaction tables, type/category filters, transaction create/edit dialogs.

## 2. Shared & UI Components
- Generic design system primitives belong in `src/components/ui/` (shadcn/ui style with Radix UI primitives).
- App-level layouts belong in `src/components/` (e.g. `AppLayout.tsx`).
- Subcomponents inside layouts must be declared as standalone components outside the render loop to prevent re-creation and loss of focus/state.

## 3. Strict Type Safety & Naming
- Never use `any`. Always define strict interfaces in `src/types/`.
- Frontend interfaces must stay in sync with backend Pydantic models.
- When icon names collide with data model names, always alias the icon (e.g. `User as UserIcon`).

## 4. UI/UX Design Standards
- **Color Semantics**:
  - Green / Emerald: Income, positive balance, budgets in healthy status (`status: "within"`).
  - Red / Destructive: Expenses, exceeded budgets (`status: "exceeded"`), delete actions.
  - Amber / Yellow: Warning thresholds (`status: "warning"`, budget usage >= 80%).
- **Confirmation Modals**: Every destructive operation (deleting a transaction, category, or budget) must be guarded with a confirmation prompt.
- **Responsive Layout**: Mobile navigation via drawer; desktop navigation via fixed sidebar.
