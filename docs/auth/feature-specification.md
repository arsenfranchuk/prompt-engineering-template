# Authentication & Authorization — Consolidated Feature Specification

## 1. Purpose & Business Requirements

Provide secure, isolated user authentication and session management for the Personal Budget Planner so that every user's financial records (income, expenses, categories, budgets, and statistics) remain completely private and accessible only to that authenticated user.

### Functional Requirements

| ID | Requirement | Scope |
|----|-------------|-------|
| BR-AUTH-01 | User registration with username, email, password, and password confirmation. | Full Stack |
| BR-AUTH-02 | Client and server-side validation: valid email, required fields, minimum password length (6+ chars), matching password confirmation. | Full Stack |
| BR-AUTH-03 | Prevent duplicate usernames and duplicate emails (unique constraint). Return descriptive error messages (HTTP 409 or 400). | Backend |
| BR-AUTH-04 | Passwords must never be stored in plain text. Secure PBKDF2-HMAC-SHA256 hashing with unique cryptographic salt per user. | Backend |
| BR-AUTH-05 | Automatically seed default income and expense categories upon successful user registration. | Backend |
| BR-AUTH-06 | User login with email or username and password. Return authentication token and user profile on success. | Full Stack |
| BR-AUTH-07 | Persistent session management: clients store token securely; server validates session token on all protected endpoints. | Full Stack |
| BR-AUTH-08 | Protected route guards: unauthorized requests return HTTP 401; frontend redirects unauthenticated visitors to `/login`. | Full Stack |
| BR-AUTH-09 | Logout invalidates client session and clears stored tokens. | Full Stack |
| BR-AUTH-10 | Strict tenant/user data isolation: every resource query strictly filters by `user_id`. Cross-user access is impossible. | Backend |

## 2. Architecture

### Backend
- **Storage**: `backend/data/users.json` and `backend/data/sessions.json`.
- **Layers**:
  - `models/user.py`: `UserRegisterRequest`, `UserLoginRequest`, `UserResponse`, `UserInDb`, `SessionInDb`.
  - `repositories/user_repository.py`: CRUD for user entities and session tokens.
  - `services/auth_service.py`: Password hashing/verification, registration flow (seeding categories), token issuance, authentication token resolution.
  - `routers/auth.py`: REST endpoints `/api/auth/register`, `/api/auth/login`, `/api/auth/logout`, `/api/auth/me`.
  - `dependencies.py`: `get_current_user` dependency extracting and validating `Authorization: Bearer <token>`.

### Frontend
- **State**: Redux `authSlice` storing `token`, `user`, `isAuthenticated`, `isLoading`.
- **API**: `authApi` endpoints (`login`, `register`, `logout`, `getMe`).
- **Base Query**: RTK Query `fetchBaseQuery` attaches `Authorization: Bearer <token>` to all API requests automatically.
- **UI Components**:
  - `LoginPage.tsx`: Email/username & password form, validation error display, demo login shortcut.
  - `RegisterPage.tsx`: Username, email, password, confirmation inputs with instant client feedback.
  - `ProtectedRoute`: Route wrapper ensuring only authenticated users can view budget and transaction pages.

## 3. Test Cases

| Test ID | Scenario | Expected Result |
|---------|----------|-----------------|
| TC-AUTH-01 | Register with valid credentials | User created, default categories seeded, token returned, HTTP 201. |
| TC-AUTH-02 | Register with existing email | Rejection with HTTP 400/409 "Email already registered". |
| TC-AUTH-03 | Register with mismatched passwords | Client blocks submit; server returns HTTP 422 if bypassed. |
| TC-AUTH-04 | Login with valid credentials | Session created, token returned, HTTP 200. |
| TC-AUTH-05 | Login with wrong password | Rejection with HTTP 401 "Invalid email/username or password". |
| TC-AUTH-06 | Access protected endpoint without token | HTTP 401 Unauthorized. |
| TC-AUTH-07 | Access protected endpoint with invalid token | HTTP 401 Unauthorized. |
| TC-AUTH-08 | User session persistence across browser reload | Token loaded from localStorage, `/api/auth/me` verifies identity. |
| TC-AUTH-09 | Logout flow | Token cleared, redirected to login page. |
