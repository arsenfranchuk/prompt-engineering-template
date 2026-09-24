# Categories — Test Cases

| ID | Test Scenario | Steps | Expected Result |
|----|---------------|-------|-----------------|
| TC-CAT-01 | View seeded categories | Log in with newly registered account and navigate to Categories | Standard income and expense categories are visible |
| TC-CAT-02 | Create custom expense category | Submit "Coffee & Snacks" as Expense category | Category created, appears under Expenses tab, HTTP 201 |
| TC-CAT-03 | Prevent duplicate category name | Submit category with an existing name for the same type | 400 Bad Request indicating name already exists |
| TC-CAT-04 | Edit category name | Rename category from "Food & Groceries" to "Groceries" | Name updated, reflects in category list and dropdowns |
| TC-CAT-05 | Safe delete rejection | Attempt to delete a category that has associated transactions | Rejection with HTTP 400 "Cannot delete category in use by transactions" |
| TC-CAT-06 | Delete unused category | Delete a newly created category without transactions | Category successfully removed, HTTP 204 |
| TC-CAT-07 | Cross-user category isolation | User B attempts to edit or delete User A's category | 404 Not Found or 403 Forbidden; User B cannot modify User A's data |
