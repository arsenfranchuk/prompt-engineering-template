# Backend Rules & Guidelines (FastAPI)

## 1. Architecture & Layering
Follow the strict layered architecture for all backend features:
1. **Models / Schemas** (`app/models/`):
   - Define data schemas with Pydantic v2.
   - Separate input payloads (`*Create`, `*Update`) from output schemas (`*Response`).
2. **Repositories** (`app/repositories/`):
   - Encapsulate all database/store interactions.
   - Access JSON persistent stores (`backend/data/<entity>.json`) via `JsonStore`.
   - Never write raw store logic or file operations inside routers or services.
3. **Services** (`app/services/`):
   - Implement all business rules, mathematical calculations, and cross-entity validations here.
   - Services must depend on repositories, not directly on routers or other transport layers.
4. **Routers** (`app/routers/`):
   - Handle HTTP requests, URL pathing, status codes, and input/output serialization.
   - Inject services and the authenticated user via FastAPI's `Depends()`.
   - Never put business logic or data storage logic directly inside route handlers.
5. **Utils** (`app/utils/`):
   - Pure utility functions (security, hashing with bcrypt, JWT token decoding/encoding, paths).

## 2. Multi-Tenancy & Data Isolation
- **Strict User Ownership**: Every database record must be associated with `user_id`.
- **Query Filtering**: All repository queries (`get_by_id`, `list`, `update`, `delete`) must verify and filter by the authenticated user's ID.
- **Never trust client IDs**: Always extract the current user identity from the JWT access token using `get_current_user` dependency.

## 3. Financial Computations & Data Integrity
- Maintain exact floating-point / decimal arithmetic consistency.
- Amounts must always be positive numeric values (`amount > 0`).
- Ensure safe category deletion: do not delete categories that have active transactions or budgets referencing them.

## 4. Dependencies, Quality Tools & Testing
- Use **uv** exclusively for package management (`uv add`, `uv run`).
- **Formatting**: `uv run ruff format .` (verify with `uv run ruff format --check .`).
- **Linting**: `uv run ruff check .` (auto-fix with `uv run ruff check --fix .`).
- **Type Checking**: `uv run mypy app`.
- **Testing**: `uv run pytest` (all tests automatically use isolated storage in `tests/conftest.py`).
- Write unit/integration tests under `tests/` covering new router endpoints, repository operations, and edge-case calculations.
