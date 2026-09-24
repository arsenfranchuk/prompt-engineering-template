# Budgets — Architecture

## Overview
Budgets compute real-time variance by pairing planned targets with live transactional expenses.

```mermaid
sequenceDiagram
  autonumber
  participant UI as BudgetsPage
  participant API as /api/budgets
  participant BService as BudgetService
  participant BRepo as BudgetRepository (budgets.json)
  participant TRepo as TransactionRepository (transactions.json)

  UI->>API: GET /api/budgets
  API->>BService: get_user_budgets(user_id)
  BService->>BRepo: find_by_user(user_id)
  BService->>TRepo: find_expenses_by_user(user_id)
  loop For Each Budget
    BService->>BService: compute spent_amount, remaining, percentage, status
  end
  BService-->>API: list[BudgetResponse]
  API-->>UI: JSON data
  UI->>UI: Render progress bars & status chips
```

## Backend Components
- `models/budget.py`: `BudgetCreate`, `BudgetUpdate`, `BudgetInDb`, `BudgetResponse` (including computed fields: `spent_amount`, `remaining_amount`, `percentage_used`, `status`).
- `repositories/budget_repository.py`: Storage in `backend/data/budgets.json`.
- `services/budget_service.py`: Computes spent amounts by joining transactions within dates; enforces validation rules.
- `routers/budgets.py`: REST endpoints: `GET /api/budgets`, `POST /api/budgets`, `GET /api/budgets/{id}`, `PATCH /api/budgets/{id}`, `DELETE /api/budgets/{id}`.

## Frontend Components
- `types/budget.ts`: Budget interfaces.
- `store/api/budgetsApi.ts`: RTK Query endpoints.
- `features/budgets/BudgetsPage.tsx`: Interactive grid of budget cards with progress meters, status tags, and action buttons.
- `features/budgets/BudgetDialog.tsx`: Modal for creating and editing budgets.
