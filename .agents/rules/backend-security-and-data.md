---
description: FastAPI backend multi-tenancy, JWT session authentication, and data isolation rules.
trigger: glob
globs: "backend/**/*"
---

# Backend Security & Data Rules

These rules govern identity verification, data isolation, and access control on the backend.

## 1. Multi-Tenancy & Data Scoping
- **Strict User Ownership**: Every entity stored in `backend/data/<entity>.json` must include a `user_id` string property.
- **Never Trust Client Payloads**: Never accept `user_id` from client request bodies or query params. Always obtain the user's ID from the verified JWT access token via the `get_current_user` FastAPI dependency.
- **Query Filtering**: Every repository operation (`get_by_id`, `list_by_user`, `update`, `delete`) must include `user_id == current_user.id` filter conditions.
- **Isolation Protection**: If a user attempts to access or modify a resource belonging to another user, return HTTP 404 (Not Found) to prevent resource enumeration.

## 2. Authentication & Passwords
- **Token Security**: Authentication uses bearer JWT tokens with expiration dates.
- **Password Protection**: Passwords must be hashed using secure algorithms (`hashlib.sha256` or bcrypt with salt). Plaintext passwords must never be stored, logged, or serialized.
- **Validation**: Enforce password strength minimums (minimum 6 characters) on registration and password change.
