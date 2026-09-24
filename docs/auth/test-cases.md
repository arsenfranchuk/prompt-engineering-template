# Authentication — Test Cases

| ID | Test Scenario | Steps | Expected Result |
|----|---------------|-------|-----------------|
| TC-AUTH-01 | Successful registration | Submit unique username, valid email, matching passwords | 201 Created, token returned, user logged in, default categories seeded |
| TC-AUTH-02 | Duplicate email registration | Submit registration with existing email | 400 Bad Request with "Email already registered" message |
| TC-AUTH-03 | Duplicate username registration | Submit registration with existing username | 400 Bad Request with "Username already taken" message |
| TC-AUTH-04 | Password mismatch validation | Enter mismatched password confirmation | Form blocked on UI; 422 Unprocessable Entity if requested via API |
| TC-AUTH-05 | Successful login | Submit registered email and valid password | 200 OK, returns token and profile data |
| TC-AUTH-06 | Login with invalid password | Submit valid email with wrong password | 401 Unauthorized with descriptive error |
| TC-AUTH-07 | Session persistence | Refresh page when logged in | App loads token from storage, `/api/auth/me` validates session without relogin |
| TC-AUTH-08 | User logout | Click logout in profile menu | Token cleared from client, user redirected to login page |
| TC-AUTH-09 | Unauthorized route protection | Visit `/dashboard` or `/transactions` without token | App automatically redirects to `/login` |
