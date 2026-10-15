from functools import lru_cache
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from app.models.user import UserInDb
from app.repositories.budget_repository import BudgetRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthenticationError, AuthService
from app.services.budget_service import BudgetService
from app.services.category_service import CategoryService
from app.services.dashboard_service import DashboardService
from app.services.transaction_service import TransactionService
from app.utils.paths import get_data_dir


@lru_cache
def get_user_repository() -> UserRepository:
    data_dir = get_data_dir()
    return UserRepository(
        users_file=data_dir / "users.json",
        sessions_file=data_dir / "sessions.json",
    )


@lru_cache
def get_category_repository() -> CategoryRepository:
    data_dir = get_data_dir()
    return CategoryRepository(file_path=data_dir / "categories.json")


@lru_cache
def get_transaction_repository() -> TransactionRepository:
    data_dir = get_data_dir()
    return TransactionRepository(file_path=data_dir / "transactions.json")


@lru_cache
def get_budget_repository() -> BudgetRepository:
    data_dir = get_data_dir()
    return BudgetRepository(file_path=data_dir / "budgets.json")


def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    cat_repo: CategoryRepository = Depends(get_category_repository),
) -> AuthService:
    return AuthService(user_repository=user_repo, category_repository=cat_repo)


def get_category_service(
    cat_repo: CategoryRepository = Depends(get_category_repository),
    tx_repo: TransactionRepository = Depends(get_transaction_repository),
    budget_repo: BudgetRepository = Depends(get_budget_repository),
) -> CategoryService:
    return CategoryService(
        category_repository=cat_repo,
        transaction_repository=tx_repo,
        budget_repository=budget_repo,
    )


def get_transaction_service(
    tx_repo: TransactionRepository = Depends(get_transaction_repository),
    cat_repo: CategoryRepository = Depends(get_category_repository),
) -> TransactionService:
    return TransactionService(
        transaction_repository=tx_repo,
        category_repository=cat_repo,
    )


def get_budget_service(
    budget_repo: BudgetRepository = Depends(get_budget_repository),
    tx_repo: TransactionRepository = Depends(get_transaction_repository),
    cat_repo: CategoryRepository = Depends(get_category_repository),
) -> BudgetService:
    return BudgetService(
        budget_repository=budget_repo,
        transaction_repository=tx_repo,
        category_repository=cat_repo,
    )


def get_dashboard_service(
    tx_repo: TransactionRepository = Depends(get_transaction_repository),
    cat_repo: CategoryRepository = Depends(get_category_repository),
    budget_repo: BudgetRepository = Depends(get_budget_repository),
) -> DashboardService:
    return DashboardService(
        transaction_repository=tx_repo,
        category_repository=cat_repo,
        budget_repository=budget_repo,
    )


def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserInDb:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided or invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization.split("Bearer ", 1)[1].strip()
    try:
        return auth_service.authenticate_token(token)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
