# Authentication — Business Requirements

## Purpose
Provide secure user registration, login, logout, and token session management so each user has an isolated, private financial account.

## Functional Requirements

| ID | Requirement | Scope |
|----|-------------|-------|
| BR-AUTH-01 | Users can register with username, email, password, and password confirmation. | Full Stack |
| BR-AUTH-02 | Client & server validation for email format, password min-length (6 chars), and passwords matching. | Full Stack |
| BR-AUTH-03 | Enforce unique usernames and emails; return human-friendly errors if already taken. | Backend |
| BR-AUTH-04 | Secure PBKDF2 password hashing with per-user salt; never store plaintext passwords. | Backend |
| BR-AUTH-05 | Automatically populate default income & expense categories upon registration. | Backend |
| BR-AUTH-06 | Users can log in using either email or username with password; receive auth token and profile. | Full Stack |
| BR-AUTH-07 | Persistent sessions stored on client (localStorage) and verified via Bearer token header. | Full Stack |
| BR-AUTH-08 | Protected routes redirect unauthenticated users to the Login page. | Frontend |
| BR-AUTH-09 | User logout clears credentials and ends session. | Full Stack |
| BR-AUTH-10 | Strict user data isolation: all resources are scoped to the authenticated `user_id`. | Backend |
