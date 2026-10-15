from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.dependencies import (
    get_budget_repository,
    get_category_repository,
    get_transaction_repository,
    get_user_repository,
)
from app.main import app
from app.repositories.budget_repository import BudgetRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository


@pytest.fixture(autouse=True)
def isolated_storage(tmp_path: Path):
    """Overrides repositories to use isolated temporary files for each test."""
    user_repo = UserRepository(
        users_file=tmp_path / "users.json",
        sessions_file=tmp_path / "sessions.json",
    )
    cat_repo = CategoryRepository(file_path=tmp_path / "categories.json")
    tx_repo = TransactionRepository(file_path=tmp_path / "transactions.json")
    budget_repo = BudgetRepository(file_path=tmp_path / "budgets.json")

    app.dependency_overrides[get_user_repository] = lambda: user_repo
    app.dependency_overrides[get_category_repository] = lambda: cat_repo
    app.dependency_overrides[get_transaction_repository] = lambda: tx_repo
    app.dependency_overrides[get_budget_repository] = lambda: budget_repo

    yield

    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "personal-budget-planner"


def test_auth_workflow(client: TestClient):
    # 1. Register User Alice
    register_payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "Password123!",
        "password_confirm": "Password123!",
    }
    r = client.post("/api/auth/register", json=register_payload)
    assert r.status_code == 201
    auth_data = r.json()
    assert "token" in auth_data
    token = auth_data["token"]
    user = auth_data["user"]
    assert user["username"] == "alice"
    assert user["email"] == "alice@example.com"
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Verify seeded default categories
    r_cats = client.get("/api/categories", headers=headers)
    assert r_cats.status_code == 200
    cats = r_cats.json()
    assert len(cats) >= 14
    expense_cats = [c for c in cats if c["type"] == "expense"]
    income_cats = [c for c in cats if c["type"] == "income"]
    assert len(expense_cats) >= 9
    assert len(income_cats) >= 5

    # 3. Duplicate checks
    r_dup_user = client.post(
        "/api/auth/register",
        json={
            "username": "alice",
            "email": "different@example.com",
            "password": "Password123!",
            "password_confirm": "Password123!",
        },
    )
    assert r_dup_user.status_code == 400
    assert "Username is already taken" in r_dup_user.json()["detail"]

    r_dup_email = client.post(
        "/api/auth/register",
        json={
            "username": "alice2",
            "email": "alice@example.com",
            "password": "Password123!",
            "password_confirm": "Password123!",
        },
    )
    assert r_dup_email.status_code == 400
    assert "Email is already registered" in r_dup_email.json()["detail"]

    # 4. Login with username
    r_login_user = client.post(
        "/api/auth/login",
        json={
            "identifier": "alice",
            "password": "Password123!",
        },
    )
    assert r_login_user.status_code == 200
    assert "token" in r_login_user.json()

    # 5. Login with email
    r_login_email = client.post(
        "/api/auth/login",
        json={
            "identifier": "alice@example.com",
            "password": "Password123!",
        },
    )
    assert r_login_email.status_code == 200

    # 6. Login invalid credentials
    r_bad_pw = client.post(
        "/api/auth/login",
        json={
            "identifier": "alice",
            "password": "WrongPassword!",
        },
    )
    assert r_bad_pw.status_code == 401

    r_bad_user = client.post(
        "/api/auth/login",
        json={
            "identifier": "nonexistent",
            "password": "Password123!",
        },
    )
    assert r_bad_user.status_code == 401

    # 7. Logout
    r_logout = client.post("/api/auth/logout", headers=headers)
    assert r_logout.status_code == 200
    # Old token should be invalidated
    r_me = client.get("/api/auth/me", headers=headers)
    assert r_me.status_code == 401


def test_user_profile_and_password(client: TestClient):
    # Register user
    r = client.post(
        "/api/auth/register",
        json={
            "username": "charlie",
            "email": "charlie@example.com",
            "password": "Password123!",
            "password_confirm": "Password123!",
        },
    )
    token = r.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get profile
    r_me = client.get("/api/auth/me", headers=headers)
    assert r_me.status_code == 200
    assert r_me.json()["username"] == "charlie"

    # Update profile
    r_patch = client.patch(
        "/api/auth/profile",
        headers=headers,
        json={
            "username": "charlie_updated",
            "email": "charlie_new@example.com",
        },
    )
    assert r_patch.status_code == 200
    assert r_patch.json()["username"] == "charlie_updated"
    assert r_patch.json()["email"] == "charlie_new@example.com"

    # Change password
    r_pw = client.post(
        "/api/auth/change-password",
        headers=headers,
        json={
            "current_password": "Password123!",
            "new_password": "NewSecretPassword123!",
            "new_password_confirm": "NewSecretPassword123!",
        },
    )
    assert r_pw.status_code == 200

    # Login with new password
    r_login = client.post(
        "/api/auth/login",
        json={
            "identifier": "charlie_updated",
            "password": "NewSecretPassword123!",
        },
    )
    assert r_login.status_code == 200


def test_categories_management(client: TestClient):
    # Register user
    r = client.post(
        "/api/auth/register",
        json={
            "username": "david",
            "email": "david@example.com",
            "password": "Password123!",
            "password_confirm": "Password123!",
        },
    )
    token = r.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create custom expense category
    r_create = client.post(
        "/api/categories",
        headers=headers,
        json={
            "name": "Coffee & Snacks",
            "type": "expense",
        },
    )
    assert r_create.status_code == 201
    cat = r_create.json()
    cat_id = cat["id"]
    assert cat["name"] == "Coffee & Snacks"
    assert cat["type"] == "expense"
    assert cat["is_default"] is False

    # Prevent duplicate category name for same type
    r_dup = client.post(
        "/api/categories",
        headers=headers,
        json={
            "name": "Coffee & Snacks",
            "type": "expense",
        },
    )
    assert r_dup.status_code == 400

    # Update category
    r_update = client.patch(
        f"/api/categories/{cat_id}",
        headers=headers,
        json={
            "name": "Coffee, Tea & Snacks",
        },
    )
    assert r_update.status_code == 200
    assert r_update.json()["name"] == "Coffee, Tea & Snacks"

    # Delete unused category
    r_del = client.delete(f"/api/categories/{cat_id}", headers=headers)
    assert r_del.status_code == 204

    # Verify category is gone
    r_get = client.get(f"/api/categories/{cat_id}", headers=headers)
    assert r_get.status_code == 404


def test_transactions_and_in_use_deletion(client: TestClient):
    # Register user
    r = client.post(
        "/api/auth/register",
        json={
            "username": "eva",
            "email": "eva@example.com",
            "password": "Password123!",
            "password_confirm": "Password123!",
        },
    )
    token = r.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch categories
    cats = client.get("/api/categories", headers=headers).json()
    salary_cat = next(c for c in cats if c["name"] == "Salary")
    groceries_cat = next(c for c in cats if c["name"] == "Food & Groceries")

    # 1. Add income transaction
    r_income = client.post(
        "/api/transactions",
        headers=headers,
        json={
            "type": "income",
            "amount": 3500.0,
            "category_id": salary_cat["id"],
            "date": "2026-09-01",
            "description": "Monthly Salary",
        },
    )
    assert r_income.status_code == 201
    inc_tx = r_income.json()
    assert inc_tx["amount"] == 3500.0
    assert inc_tx["category_name"] == "Salary"

    # 2. Add expense transaction
    r_expense = client.post(
        "/api/transactions",
        headers=headers,
        json={
            "type": "expense",
            "amount": 120.50,
            "category_id": groceries_cat["id"],
            "date": "2026-09-05",
            "description": "Weekly supermarket shopping",
        },
    )
    assert r_expense.status_code == 201
    exp_tx = r_expense.json()
    assert exp_tx["amount"] == 120.50
    assert exp_tx["category_name"] == "Food & Groceries"

    # 3. Reject mismatching category type
    r_mismatch = client.post(
        "/api/transactions",
        headers=headers,
        json={
            "type": "income",
            "amount": 500.0,
            "category_id": groceries_cat["id"],  # Expense category for income
            "date": "2026-09-10",
            "description": "Invalid",
        },
    )
    assert r_mismatch.status_code == 400

    # 4. List transactions with filters
    r_list_exp = client.get("/api/transactions?type=expense", headers=headers)
    assert r_list_exp.status_code == 200
    assert len(r_list_exp.json()) == 1
    assert r_list_exp.json()[0]["id"] == exp_tx["id"]

    r_list_search = client.get("/api/transactions?search=supermarket", headers=headers)
    assert r_list_search.status_code == 200
    assert len(r_list_search.json()) == 1

    # 5. Prevent deleting category that has transactions
    r_del_cat = client.delete(f"/api/categories/{groceries_cat['id']}", headers=headers)
    assert r_del_cat.status_code == 400
    assert "associated transaction" in r_del_cat.json()["detail"]

    # 6. Update transaction
    r_update_tx = client.patch(
        f"/api/transactions/{exp_tx['id']}",
        headers=headers,
        json={
            "amount": 135.0,
            "description": "Updated supermarket shopping",
        },
    )
    assert r_update_tx.status_code == 200
    assert r_update_tx.json()["amount"] == 135.0

    # 7. Delete transaction
    r_del_tx = client.delete(f"/api/transactions/{exp_tx['id']}", headers=headers)
    assert r_del_tx.status_code == 204


def test_budgets_and_calculations(client: TestClient):
    # Register user
    r = client.post(
        "/api/auth/register",
        json={
            "username": "frank",
            "email": "frank@example.com",
            "password": "Password123!",
            "password_confirm": "Password123!",
        },
    )
    token = r.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    cats = client.get("/api/categories", headers=headers).json()
    housing_cat = next(c for c in cats if c["name"] == "Housing & Rent")
    salary_cat = next(c for c in cats if c["name"] == "Salary")

    now = datetime.now(UTC)
    current_month_str = f"{now.year:04d}-{now.month:02d}-01"

    # Reject budget for income category
    r_bad_b = client.post(
        "/api/budgets",
        headers=headers,
        json={
            "category_id": salary_cat["id"],
            "planned_amount": 1000.0,
            "period": "monthly",
            "start_date": current_month_str,
        },
    )
    assert r_bad_b.status_code == 400
    assert "Budgets can only be created for expense categories" in r_bad_b.json()["detail"]

    # Create valid budget: 1000.0 planned
    r_budget = client.post(
        "/api/budgets",
        headers=headers,
        json={
            "category_id": housing_cat["id"],
            "planned_amount": 1000.0,
            "period": "monthly",
            "start_date": current_month_str,
        },
    )
    assert r_budget.status_code == 201
    b_data = r_budget.json()
    assert b_data["planned_amount"] == 1000.0
    assert b_data["spent_amount"] == 0.0
    assert b_data["remaining_amount"] == 1000.0
    assert b_data["status"] == "within"

    # Add transaction under housing_cat: 500.0
    client.post(
        "/api/transactions",
        headers=headers,
        json={
            "type": "expense",
            "amount": 500.0,
            "category_id": housing_cat["id"],
            "date": f"{now.year:04d}-{now.month:02d}-15",
            "description": "Rent part 1",
        },
    )

    # Check budget metrics after 500 spent (50% -> 'within')
    b_check1 = client.get(f"/api/budgets/{b_data['id']}", headers=headers).json()
    assert b_check1["spent_amount"] == 500.0
    assert b_check1["remaining_amount"] == 500.0
    assert b_check1["percentage_used"] == 50.0
    assert b_check1["status"] == "within"

    # Add another expense: 400.0 (total 900 spent = 90% -> 'warning')
    client.post(
        "/api/transactions",
        headers=headers,
        json={
            "type": "expense",
            "amount": 400.0,
            "category_id": housing_cat["id"],
            "date": f"{now.year:04d}-{now.month:02d}-20",
            "description": "Rent part 2",
        },
    )
    b_check2 = client.get(f"/api/budgets/{b_data['id']}", headers=headers).json()
    assert b_check2["spent_amount"] == 900.0
    assert b_check2["status"] == "warning"

    # Add another expense: 200.0 (total 1100 spent = 110% -> 'exceeded')
    client.post(
        "/api/transactions",
        headers=headers,
        json={
            "type": "expense",
            "amount": 200.0,
            "category_id": housing_cat["id"],
            "date": f"{now.year:04d}-{now.month:02d}-22",
            "description": "Rent fee",
        },
    )
    b_check3 = client.get(f"/api/budgets/{b_data['id']}", headers=headers).json()
    assert b_check3["spent_amount"] == 1100.0
    assert b_check3["remaining_amount"] == -100.0
    assert b_check3["status"] == "exceeded"


def test_dashboard_summary_and_statistics(client: TestClient):
    r = client.post(
        "/api/auth/register",
        json={
            "username": "grace",
            "email": "grace@example.com",
            "password": "Password123!",
            "password_confirm": "Password123!",
        },
    )
    token = r.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    cats = client.get("/api/categories", headers=headers).json()
    salary = next(c for c in cats if c["name"] == "Salary")
    food = next(c for c in cats if c["name"] == "Food & Groceries")
    bills = next(c for c in cats if c["name"] == "Utilities & Bills")

    now = datetime.now(UTC)
    cur_date = f"{now.year:04d}-{now.month:02d}-10"

    # Income 4000
    client.post(
        "/api/transactions",
        headers=headers,
        json={
            "type": "income",
            "amount": 4000.0,
            "category_id": salary["id"],
            "date": cur_date,
            "description": "Full salary",
        },
    )

    # Expenses: 600 food, 400 bills = 1000 total
    client.post(
        "/api/transactions",
        headers=headers,
        json={
            "type": "expense",
            "amount": 600.0,
            "category_id": food["id"],
            "date": cur_date,
            "description": "Groceries",
        },
    )
    client.post(
        "/api/transactions",
        headers=headers,
        json={
            "type": "expense",
            "amount": 400.0,
            "category_id": bills["id"],
            "date": cur_date,
            "description": "Electricity",
        },
    )

    # Check dashboard summary
    r_dash = client.get("/api/dashboard/summary?period=current_month", headers=headers)
    assert r_dash.status_code == 200
    dash = r_dash.json()

    assert dash["current_balance"] == 3000.0
    assert dash["period_income"] == 4000.0
    assert dash["period_expenses"] == 1000.0
    assert dash["period_net"] == 3000.0
    assert dash["savings_rate"] == 75.0
    assert len(dash["spending_by_category"]) == 2
    assert dash["spending_by_category"][0]["amount"] == 600.0
    assert dash["spending_by_category"][0]["percentage"] == 60.0
    assert len(dash["recent_transactions"]) == 3
    assert len(dash["monthly_trend"]) == 6


def test_user_data_isolation(client: TestClient):
    """Ensures that one user can never view or manipulate another user's financial data."""
    # User 1: User Alpha
    r1 = client.post(
        "/api/auth/register",
        json={
            "username": "alpha",
            "email": "alpha@example.com",
            "password": "Password123!",
            "password_confirm": "Password123!",
        },
    )
    token1 = r1.json()["token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    # User 2: User Beta
    r2 = client.post(
        "/api/auth/register",
        json={
            "username": "beta",
            "email": "beta@example.com",
            "password": "Password123!",
            "password_confirm": "Password123!",
        },
    )
    token2 = r2.json()["token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Alpha creates custom category, transaction, and budget
    alpha_cat = client.post(
        "/api/categories",
        headers=headers1,
        json={
            "name": "Alpha Private Category",
            "type": "expense",
        },
    ).json()

    alpha_tx = client.post(
        "/api/transactions",
        headers=headers1,
        json={
            "type": "expense",
            "amount": 999.0,
            "category_id": alpha_cat["id"],
            "date": "2026-09-12",
            "description": "Alpha Private Transaction",
        },
    ).json()

    alpha_budget = client.post(
        "/api/budgets",
        headers=headers1,
        json={
            "category_id": alpha_cat["id"],
            "planned_amount": 2000.0,
            "period": "monthly",
            "start_date": "2026-09-01",
        },
    ).json()

    # Beta attempts to read Alpha's custom category -> cannot see it in list
    beta_cats = client.get("/api/categories", headers=headers2).json()
    assert not any(c["name"] == "Alpha Private Category" for c in beta_cats)

    # Beta attempts to get Alpha's category by ID -> 404
    r_cat_access = client.get(f"/api/categories/{alpha_cat['id']}", headers=headers2)
    assert r_cat_access.status_code == 404

    # Beta attempts to read Alpha's transaction list -> should not be there
    beta_txs = client.get("/api/transactions", headers=headers2).json()
    assert not any(t["id"] == alpha_tx["id"] for t in beta_txs)

    # Beta attempts to get, patch, delete Alpha's transaction -> 404
    assert client.get(f"/api/transactions/{alpha_tx['id']}", headers=headers2).status_code == 404
    assert (
        client.patch(
            f"/api/transactions/{alpha_tx['id']}", headers=headers2, json={"amount": 1.0}
        ).status_code
        == 404
    )
    assert client.delete(f"/api/transactions/{alpha_tx['id']}", headers=headers2).status_code == 404

    # Beta attempts to read Alpha's budget list -> should not be there
    beta_budgets = client.get("/api/budgets", headers=headers2).json()
    assert not any(b["id"] == alpha_budget["id"] for b in beta_budgets)

    # Beta attempts to get, patch, delete Alpha's budget -> 404
    assert client.get(f"/api/budgets/{alpha_budget['id']}", headers=headers2).status_code == 404
    assert (
        client.patch(
            f"/api/budgets/{alpha_budget['id']}", headers=headers2, json={"planned_amount": 1.0}
        ).status_code
        == 404
    )
    assert client.delete(f"/api/budgets/{alpha_budget['id']}", headers=headers2).status_code == 404

    # Beta's dashboard should be completely zero
    beta_dash = client.get("/api/dashboard/summary?period=all", headers=headers2).json()
    assert beta_dash["current_balance"] == 0.0
    assert beta_dash["period_income"] == 0.0
    assert beta_dash["period_expenses"] == 0.0
    assert len(beta_dash["recent_transactions"]) == 0
