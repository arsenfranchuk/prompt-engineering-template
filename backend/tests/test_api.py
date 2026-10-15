import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_full_flow():
    now = datetime.now(UTC)
    cur_date_01 = f"{now.year:04d}-{now.month:02d}-01"
    cur_date_05 = f"{now.year:04d}-{now.month:02d}-05"
    cur_date_10 = f"{now.year:04d}-{now.month:02d}-10"

    print("Testing health...")
    r = client.get("/health")
    assert r.status_code == 200, r.text
    assert r.json()["status"] == "ok"
    print("Health OK")

    # 1. Register User 1
    print("Testing registration...")
    u1_reg = {
        "username": "alice_budget",
        "email": "alice@example.com",
        "password": "Password123!",
        "password_confirm": "Password123!",
    }
    r = client.post("/api/auth/register", json=u1_reg)
    assert r.status_code == 201, r.text
    data = r.json()
    token1 = data["token"]
    user1_id = data["user"]["id"]
    headers1 = {"Authorization": f"Bearer {token1}"}
    print("Registration OK. User1 ID:", user1_id)

    # Duplicate registration check
    r = client.post("/api/auth/register", json=u1_reg)
    assert r.status_code == 400, "Should reject duplicate"
    print("Duplicate rejection OK")

    # 2. Check Seeded Categories for User 1
    r = client.get("/api/categories", headers=headers1)
    assert r.status_code == 200
    cats1 = r.json()
    assert len(cats1) >= 10, f"Expected seeded categories, got {len(cats1)}"
    salary_cat = next(c for c in cats1 if c["name"] == "Salary")
    food_cat = next(c for c in cats1 if c["name"] == "Food & Groceries")
    print(f"Categories seeded OK: {len(cats1)} categories found")

    # 3. Add Custom Category
    r = client.post("/api/categories", headers=headers1, json={"name": "Coffee", "type": "expense"})
    assert r.status_code == 201
    coffee_cat = r.json()
    print("Custom category created OK:", coffee_cat["name"])

    # 4. Add Income Transaction
    r = client.post(
        "/api/transactions",
        headers=headers1,
        json={
            "type": "income",
            "amount": 5000.0,
            "category_id": salary_cat["id"],
            "date": cur_date_01,
            "description": "Monthly Salary",
        },
    )
    assert r.status_code == 201
    tx_income = r.json()
    print("Income transaction OK:", tx_income["amount"])

    # 5. Add Expense Transactions
    r = client.post(
        "/api/transactions",
        headers=headers1,
        json={
            "type": "expense",
            "amount": 250.0,
            "category_id": food_cat["id"],
            "date": cur_date_05,
            "description": "Weekly grocery shopping",
        },
    )
    assert r.status_code == 201

    r = client.post(
        "/api/transactions",
        headers=headers1,
        json={
            "type": "expense",
            "amount": 50.0,
            "category_id": coffee_cat["id"],
            "date": cur_date_10,
            "description": "Espresso beans",
        },
    )
    assert r.status_code == 201

    # 6. Check Dashboard Summary
    r = client.get("/api/dashboard/summary?period=current_month", headers=headers1)
    assert r.status_code == 200
    dash = r.json()
    assert dash["current_balance"] == 4700.0, (
        f"Expected 4700.0 balance, got {dash['current_balance']}"
    )
    assert dash["period_income"] == 5000.0
    assert dash["period_expenses"] == 300.0
    assert dash["period_net"] == 4700.0
    print("Dashboard calculations OK! Balance:", dash["current_balance"])

    # 7. Create Budget for Food
    r = client.post(
        "/api/budgets",
        headers=headers1,
        json={
            "category_id": food_cat["id"],
            "planned_amount": 500.0,
            "period": "monthly",
            "start_date": cur_date_01,
        },
    )
    assert r.status_code == 201
    budget_food = r.json()
    assert budget_food["spent_amount"] == 250.0, (
        f"Expected 250.0 spent, got {budget_food['spent_amount']}"
    )
    assert budget_food["remaining_amount"] == 250.0
    assert budget_food["percentage_used"] == 50.0
    assert budget_food["status"] == "within"
    print(
        "Budget metrics OK! Spent:", budget_food["spent_amount"], "Status:", budget_food["status"]
    )

    # 8. Safe Category Deletion Test
    r = client.delete(f"/api/categories/{coffee_cat['id']}", headers=headers1)
    assert r.status_code == 400, "Should not delete category in use by transaction"
    print("Safe category deletion check passed!")

    # 9. Multi-User Isolation Test (Register Bob)
    u2_reg = {
        "username": "bob_trader",
        "email": "bob@example.com",
        "password": "SecretPassword123!",
        "password_confirm": "SecretPassword123!",
    }
    r = client.post("/api/auth/register", json=u2_reg)
    assert r.status_code == 201
    token2 = r.json()["token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Bob checks dashboard - should have 0 balance
    r = client.get("/api/dashboard/summary", headers=headers2)
    assert r.status_code == 200
    bob_dash = r.json()
    assert bob_dash["current_balance"] == 0.0, "Bob's balance should be 0.0"

    # Bob cannot access Alice's transaction
    r = client.get(f"/api/transactions/{tx_income['id']}", headers=headers2)
    assert r.status_code == 404, "Bob should not see Alice's transaction"

    # Bob cannot delete Alice's budget
    r = client.delete(f"/api/budgets/{budget_food['id']}", headers=headers2)
    assert r.status_code == 404, "Bob should not be able to delete Alice's budget"

    print("Multi-user isolation test passed!")
    print("ALL BACKEND TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_full_flow()
