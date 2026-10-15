---
description: FastAPI backend layered architecture, Pydantic v2 schemas, and repository covariance rules.
trigger: glob
globs: "backend/**/*"
---

# Backend Architecture & Layering Rules

These rules govern the architectural layout and dependency boundaries of the FastAPI backend in `backend/`.

## 1. Five-Layer Architecture
Backend code must strictly adhere to the following layers without skipping or leaking responsibilities:

1. **Routers (`app/routers/`)**:
   - Sole responsibility: HTTP protocol handling, URL routing, query/path parameter parsing, status code responses, and serialization.
   - Inject dependencies (`Service`, `current_user`) using FastAPI's `Depends()`.
   - **Prohibited**: Direct business logic calculations, file I/O, or calling repositories directly.

2. **Services (`app/services/`)**:
   - Sole responsibility: Business domain logic, financial computations, multi-entity validations, and workflows.
   - Throw domain-specific exceptions (e.g. `InvalidTransactionDataError`, `CategoryInUseError`, `BudgetNotFoundError`).
   - Depend only on Repositories and models.
   - **Prohibited**: Accessing FastAPI `Request`/`Response` objects or calling raw storage helpers.

3. **Repositories (`app/repositories/`)**:
   - Sole responsibility: Persistence operations on JSON stores (`backend/data/<entity>.json`).
   - Access stores via `app.utils.json_store` (`read_list_file`, `write_list_file`).
   - Accept `Sequence[BaseModel]` in write methods to ensure list covariance.
   - **Prohibited**: Implementing business rules or cross-entity validations.

4. **Models & Schemas (`app/models/`)**:
   - Define all models using Pydantic v2.
   - Strictly separate model schemas:
     - `*Base`: Shared field definitions.
     - `*Create`: Input payload for creation.
     - `*Update`: Input payload for partial updates (all fields optional).
     - `*InDb`: Internal storage entity with `id`, `user_id`, `created_at`, `updated_at`.
     - `*Response`: Serialization model returned to HTTP clients.

5. **Utilities (`app/utils/`)**:
   - Pure helpers with minimal state: `json_store.py`, `security.py`.

## 2. Financial Computations & Integrity
- **Positive Amounts**: Transaction amounts and budget planned amounts must strictly be positive (`amount > 0`).
- **Precision**: Round all financial amounts and balances to 2 decimal places (`round(amount, 2)`).
- **Safe Category Deletion**: Categories cannot be deleted if referenced by active transactions or budgets. The service must raise `CategoryInUseError`.
