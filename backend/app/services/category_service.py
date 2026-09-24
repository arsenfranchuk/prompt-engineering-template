from app.models.category import (
    CategoryCreate,
    CategoryInDb,
    CategoryResponse,
    CategoryUpdate,
)
from app.repositories.budget_repository import BudgetRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.transaction_repository import TransactionRepository


class CategoryNotFoundError(Exception):
    pass


class CategoryDuplicateError(Exception):
    pass


class CategoryInUseError(Exception):
    pass


class CategoryService:
    def __init__(
        self,
        category_repository: CategoryRepository,
        transaction_repository: TransactionRepository,
        budget_repository: BudgetRepository,
    ) -> None:
        self._cat_repo = category_repository
        self._tx_repo = transaction_repository
        self._budget_repo = budget_repository

    def list_categories(self, user_id: str) -> list[CategoryResponse]:
        # Always ensure defaults exist
        user_cats = self._cat_repo.list_by_user(user_id)
        if not user_cats:
            user_cats = self._cat_repo.seed_defaults_for_user(user_id)
        return [CategoryResponse.from_db(c) for c in user_cats]

    def get_category(self, user_id: str, category_id: str) -> CategoryResponse:
        cat = self._cat_repo.get_by_id(category_id)
        if not cat or cat.user_id != user_id:
            raise CategoryNotFoundError(f"Category {category_id} not found")
        return CategoryResponse.from_db(cat)

    def create_category(self, user_id: str, payload: CategoryCreate) -> CategoryResponse:
        # Check duplicate name for this user and type
        existing_cats = self._cat_repo.list_by_user(user_id)
        if any(
            c.name.strip().lower() == payload.name.strip().lower() and c.type == payload.type
            for c in existing_cats
        ):
            raise CategoryDuplicateError(
                f"A {payload.type} category named '{payload.name}' already exists"
            )

        cat_in_db = CategoryInDb(
            user_id=user_id,
            name=payload.name,
            type=payload.type,
            is_default=False,
        )
        created = self._cat_repo.create(cat_in_db)
        return CategoryResponse.from_db(created)

    def update_category(
        self, user_id: str, category_id: str, payload: CategoryUpdate
    ) -> CategoryResponse:
        cat = self._cat_repo.get_by_id(category_id)
        if not cat or cat.user_id != user_id:
            raise CategoryNotFoundError(f"Category {category_id} not found")

        # Check duplicate name
        existing_cats = self._cat_repo.list_by_user(user_id)
        if any(
            c.id != category_id
            and c.name.strip().lower() == payload.name.strip().lower()
            and c.type == cat.type
            for c in existing_cats
        ):
            raise CategoryDuplicateError(
                f"A {cat.type} category named '{payload.name}' already exists"
            )

        cat.name = payload.name
        updated = self._cat_repo.update(cat)
        return CategoryResponse.from_db(updated)

    def delete_category(self, user_id: str, category_id: str) -> None:
        cat = self._cat_repo.get_by_id(category_id)
        if not cat or cat.user_id != user_id:
            raise CategoryNotFoundError(f"Category {category_id} not found")

        # Safe delete: check if used in transactions or budgets
        tx_count = self._tx_repo.count_by_category(category_id)
        if tx_count > 0:
            raise CategoryInUseError(
                f"Cannot delete category '{cat.name}' because it has {tx_count} associated transaction(s)."
            )

        budget_count = self._budget_repo.count_by_category(category_id)
        if budget_count > 0:
            raise CategoryInUseError(
                f"Cannot delete category '{cat.name}' because an active budget is configured for it."
            )

        self._cat_repo.delete(category_id)
