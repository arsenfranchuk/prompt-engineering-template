# Authentication — Architecture

## Overview
Full-stack authentication system bridging FastAPI session verification and React Redux client-side state.

```mermaid
sequenceDiagram
  autonumber
  actor User
  participant UI as React UI (Login/Register)
  participant Redux as authSlice & authApi
  participant API as FastAPI Router (/api/auth)
  participant Svc as AuthService
  participant Repo as UserRepository & SessionStore
  participant DB as users.json / sessions.json

  User->>UI: Submit credentials
  UI->>Redux: login/register mutation
  Redux->>API: POST /api/auth/login
  API->>Svc: authenticate(email/username, password)
  Svc->>Repo: find_by_email_or_username()
  Repo->>DB: Read users.json
  Svc->>Svc: verify_password(hash, salt)
  Svc->>Repo: create_session(user_id)
  Repo->>DB: Write sessions.json
  Svc-->>API: AuthResponse(token, user)
  API-->>Redux: HTTP 200 { token, user }
  Redux->>Redux: Save token to localStorage & state
  Redux-->>UI: Authenticated state -> Redirect to Dashboard
```

## Backend Components
- `app/models/user.py`: `UserRegisterRequest`, `UserLoginRequest`, `UserResponse`, `UserInDb`, `SessionInDb`.
- `app/repositories/user_repository.py`: File-backed storage for users and session tokens.
- `app/services/auth_service.py`: Password hashing (PBKDF2-HMAC-SHA256), verification, category seeding, token resolution.
- `app/routers/auth.py`: Endpoints for register, login, logout, me.
- `app/dependencies.py`: `get_current_user` FastAPI dependency checking `Authorization: Bearer <token>`.

## Frontend Components
- `src/types/auth.ts`: TypeScript contracts for user credentials, tokens, and payloads.
- `src/store/slices/authSlice.ts`: Token, user entity, persistent authentication state.
- `src/store/api/authApi.ts`: RTK Query endpoints with automatic token header injection.
- `src/features/auth/LoginPage.tsx` & `RegisterPage.tsx`: Form UI with instant validation and error banners.
