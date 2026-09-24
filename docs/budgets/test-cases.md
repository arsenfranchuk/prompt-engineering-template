# Budgets — Test Cases

| ID | Test Scenario | Steps | Expected Result |
|----|---------------|-------|-----------------|
| TC-BDG-01 | Create budget | Create $500 monthly budget for "Food & Groceries" | 201 Created; initial spent amount equals existing matching expenses |
| TC-BDG-02 | Spending update reflection | Add a $100 expense in "Food & Groceries" | Budget spent amount increases by $100; remaining budget decreases by $100 |
| TC-BDG-03 | Warning status threshold | Expense total reaches 85% of planned amount | Budget status changes to `warning`; bar color turns amber/yellow |
| TC-BDG-04 | Exceeded status threshold | Expense total exceeds 100% of planned amount | Budget status changes to `exceeded`; bar color turns red; shows overspent amount |
| TC-BDG-05 | Edit budget amount | Increase planned budget from $500 to $700 | Budget percentage recalculated immediately; status updates back to `within` |
| TC-BDG-06 | Delete budget | Confirm deletion of budget | Budget removed without deleting transactions; HTTP 204 |
| TC-BDG-07 | Isolation verification | User B queries User A's budget ID | 404 Not Found |
