# Transactions — Business Requirements

## Purpose
Allow users to record and manage financial transactions (Income and Expenses), search, filter by multiple criteria, sort, view details, and maintain an accurate financial ledger.

## Functional Requirements

| ID | Requirement | Scope |
|----|-------------|-------|
| BR-TX-01 | Create income or expense transactions with amount, category, date, and optional description. | Full Stack |
| BR-TX-02 | Validate required fields: amount must be positive (> 0), category must exist and match transaction type, date must be valid. | Full Stack |
| BR-TX-03 | List transactions for authenticated user with pagination or list view, showing type indicator (+ / -), amount, category, date, and description. | Full Stack |
| BR-TX-04 | Filter transactions by transaction type (`all`, `income`, `expense`). | Full Stack |
| BR-TX-05 | Filter transactions by category ID. | Full Stack |
| BR-TX-06 | Filter transactions by date range (`start_date`, `end_date`). | Full Stack |
| BR-TX-07 | Search transactions by description keyword or category name. | Full Stack |
| BR-TX-08 | Sort transactions by date (newest/oldest) or amount (highest/lowest). | Full Stack |
| BR-TX-09 | Edit an existing transaction's details (amount, category, date, description). | Full Stack |
| BR-TX-10 | Delete transaction with explicit confirmation step; recalculates user balance and budget spending. | Full Stack |
| BR-TX-11 | Strict user privacy: only the transaction owner can view, update, or delete it. | Backend |
