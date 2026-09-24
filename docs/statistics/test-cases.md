# Statistics & Analytics — Test Cases

| Test ID | Title | Preconditions | Steps | Expected Result |
|---------|-------|---------------|-------|-----------------|
| TC-STAT-01 | Current Month Balance & Net | User logged in with income and expenses in current month | Call `GET /api/dashboard/summary?period=current_month` | Total income, expenses, and net reflect current month transactions; balance reflects all-time sum. |
| TC-STAT-02 | Category Expense Distribution | User has expenses in multiple categories | Request summary | `spending_by_category` sums correctly to total period expenses and calculates accurate percentage shares. |
| TC-STAT-03 | Category Income Distribution | User has income in multiple categories | Request summary | `income_by_category` sums correctly to total period income. |
| TC-STAT-04 | Period Switching | User switches period to `previous_month` or `current_year` | Call endpoint with respective period parameter | Financial sums only encompass transactions falling within the specified period date bounds. |
| TC-STAT-05 | 6-Month Monthly Trends | Historical transactions across recent months exist | Inspect `monthly_trend` field | Returns ordered array of 6 monthly summaries with correct income, expense, and net values. |
| TC-STAT-06 | Multi-User Isolation | User A has transactions, User B has none | User B requests summary | User B receives `0.0` for all metrics and empty category breakdown arrays. |
