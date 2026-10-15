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
