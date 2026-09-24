# Transactions — Test Cases

| ID | Test Scenario | Steps | Expected Result |
|----|---------------|-------|-----------------|
| TC-TX-01 | Create income transaction | Add income with amount $3,000, category "Salary", today's date | 201 Created; appears in transaction table with green positive badge |
| TC-TX-02 | Create expense transaction | Add expense with amount $45.50, category "Food & Groceries" | 201 Created; appears in transaction table with red negative badge |
| TC-TX-03 | Amount validation | Attempt to enter $0 or negative amount | Validation blocks submission; error indicates amount must be > 0 |
| TC-TX-04 | Type filtering | Toggle filter to "Income only" | Only income transactions displayed in list |
| TC-TX-05 | Category filtering | Select specific category filter (e.g. "Housing") | Only transactions belonging to selected category displayed |
| TC-TX-06 | Search functionality | Enter keyword in search input | Matching transactions by description or category name returned |
| TC-TX-07 | Sorting | Sort by Amount descending | Transactions ordered from highest to lowest monetary value |
| TC-TX-08 | Edit transaction | Modify amount from $45.50 to $50.00 | Updated record saved; total balance and budget spending recalculate |
| TC-TX-09 | Delete transaction | Confirm deletion of transaction | Record removed from list and JSON store; balance adjusts accordingly |
| TC-TX-10 | Isolation check | User B requests User A's transaction by ID | 404 Not Found; access denied |
