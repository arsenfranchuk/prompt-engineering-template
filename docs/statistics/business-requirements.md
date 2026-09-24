# Statistics & Analytics — Business Requirements

## Purpose
Provide users with comprehensive visual and numerical insights into their personal finances across different time horizons, broken down by category, budget progress, and historical trends.

## Functional Requirements

| ID | Requirement | Scope |
|----|-------------|-------|
| BR-STAT-01 | Period filtering: allow users to inspect finances for `current_month`, `previous_month`, `current_year`, and `all` time. | Full Stack |
| BR-STAT-02 | Key financial metrics: compute and display Total Income, Total Expenses, Net Savings, and Savings Rate percentage. | Full Stack |
| BR-STAT-03 | Expense breakdown: display list and percentage distribution of spending by category for the selected period. | Full Stack |
| BR-STAT-04 | Income breakdown: display list and percentage distribution of income sources by category for the selected period. | Full Stack |
| BR-STAT-05 | Monthly trends: compute historical monthly income, expenses, and net savings for the past 6 months. | Backend & UI |
| BR-STAT-06 | Budget usage overview: show current active budget utilization percentage and alert states (within, warning, exceeded). | Full Stack |
| BR-STAT-07 | User privacy & isolation: statistics must be calculated strictly from the authenticated user's own transactions and budgets. | Backend |
