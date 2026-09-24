# Profile & Settings — Test Cases

| ID | Test Scenario | Steps | Expected Result |
|----|---------------|-------|-----------------|
| TC-PRF-01 | View profile details | Open Profile page | Displays username, email, and formatted member join date |
| TC-PRF-02 | Update username | Change username to a new valid name and save | Username successfully updated and reflected in UI header |
| TC-PRF-03 | Change password success | Provide correct current password and valid matching new password | Password updated; future logins require new password |
| TC-PRF-04 | Change password invalid current | Provide incorrect current password | 400 Bad Request: "Current password is incorrect" |
| TC-PRF-05 | Logout | Click logout button | Session cleared; redirected to login screen |
