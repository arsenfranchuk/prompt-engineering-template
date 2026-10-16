---
description: Shared cross-cutting fullstack rules, zero-defect policy, git conventions, and documentation standards.
always_on: true
---

# Shared Project Rules

These cross-cutting rules apply across the entire full-stack project (backend, frontend, and repository root).

## 1. Zero-Defect Quality Policy
- Every change must pass automated verification without errors or warnings:
  - Backend: Ruff format, Ruff check, Mypy, and Pytest.
  - Frontend: Oxlint lint, Prettier check, TypeScript typecheck, and Vite build.
- Do not disable linting rules or ignore type errors without explicit approval.

## 2. Multi-Tenancy & Security
- Strict user data isolation by `user_id`.
- Never trust client IDs from URL query or JSON body; extract identity exclusively from the authenticated JWT session.
- Never commit hardcoded secrets, private keys, or API tokens to source control.

## 3. Persistent Data Protection
- Direct manual editing of entity storage in `backend/data/*.json` is strictly prohibited.
- Lockfiles (`uv.lock` and `package-lock.json`) must be managed via their respective package managers (`uv` and `npm`).

## 4. Documentation & Feature Delivery
- Every new feature must be documented in `docs/<feature>/` covering business requirements, architecture, and test cases.
- Maintain documentation integrity: do not delete existing comments or documentation unless explicitly requested.
