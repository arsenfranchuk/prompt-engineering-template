# Categories — Business Requirements

## Purpose
Allow users to organize financial transactions and budgets into distinct Income and Expense categories. Provide pre-seeded defaults and allow users to create, modify, and safely delete custom categories.

## Functional Requirements

| ID | Requirement | Scope |
|----|-------------|-------|
| BR-CAT-01 | Support separate categories for `income` and `expense` types. | Full Stack |
| BR-CAT-02 | Seed standard categories on account creation (e.g. Salary, Freelance, Food & Groceries, Housing, Transport, Utilities, Entertainment, Healthcare). | Backend |
| BR-CAT-03 | Allow users to create custom categories with a name and type (`income` or `expense`). | Full Stack |
| BR-CAT-04 | Validate category name (non-empty, trimmed, max 50 chars) and prevent duplicates within the same type for that user. | Full Stack |
| BR-CAT-05 | Allow users to edit their own category names. | Full Stack |
| BR-CAT-06 | Safe deletion: prevent deletion of any category that is currently linked to existing transactions or active budgets. | Backend & UI |
| BR-CAT-07 | Strict data isolation: categories belong strictly to the authenticated user; users cannot view, modify, or delete another user's categories. | Backend |
