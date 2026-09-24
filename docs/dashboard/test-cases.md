# Dashboard & Analytics — Test Cases

| ID | Test Scenario | Steps | Expected Result |
|----|---------------|-------|-----------------|
| TC-DSH-01 | Current balance accuracy | Add $1,000 Income and $250 Expense | Current balance displays exactly $750.00 |
| TC-DSH-02 | Period filtering | Toggle period between "Current Month" and "Current Year" | Metrics update to reflect transactions falling within the respective dates |
| TC-DSH-03 | Quick action "+ Add Income" | Click "+ Add Income" on dashboard | Opens transaction dialog preselected to "Income" type |
| TC-DSH-04 | Quick action "+ Add Expense" | Click "+ Add Expense" on dashboard | Opens transaction dialog preselected to "Expense" type |
| TC-DSH-05 | Quick action "+ Set Budget" | Click "+ Set Budget" on dashboard | Opens budget creation modal |
| TC-DSH-06 | Category breakdown | Add multiple expenses across "Groceries" and "Utilities" | Category progress list shows accurate sums and percentage shares |
| TC-DSH-07 | Empty state | Newly registered user with no transactions views dashboard | Balance $0.00, clean empty states inviting user to add first transaction |
| TC-DSH-08 | Isolation check | User B views dashboard | Only User B's metrics are shown; completely separated from User A |
