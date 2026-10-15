from datetime import UTC, datetime

from app.models.budget import (
    BudgetCreate,
    BudgetInDb,
    BudgetResponse,
    BudgetStatus,
    BudgetUpdate,
)
from app.repositories.budget_repository import BudgetRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.transaction_repository import TransactionRepository


class BudgetNotFoundError(Exception):
    pass


class InvalidBudgetDataError(Exception):
    pass


class BudgetService:
    def __init__(
        self,
        budget_repository: BudgetRepository,
        transaction_repository: TransactionRepository,
        category_repository: CategoryRepository,
    ) -> None:
        self._budget_repo = budget_repository
        self._tx_repo = transaction_repository
        self._cat_repo = category_repository

    def _calculate_budget_metrics(
        self, budget: BudgetInDb, user_id: str
    ) -> tuple[str, float, float, float, BudgetStatus]:
        category = self._cat_repo.get_by_id(budget.category_id)
        cat_name = category.name if category else "Unknown Category"

        all_txs = self._tx_repo.list_by_user(user_id)
        # Filter transactions matching category, type='expense', and period date range
        matching_expenses = [
            t for t in all_txs if t.category_id == budget.category_id and t.type == "expense"
        ]

        if budget.period == "monthly":
            # Match YYYY-MM
            month_prefix = budget.start_date[:7]
            matching_expenses = [t for t in matching_expenses if t.date.startswith(month_prefix)]
        else:
            if budget.start_date:
                matching_expenses = [t for t in matching_expenses if t.date >= budget.start_date]
            if budget.end_date:
                matching_expenses = [t for t in matching_expenses if t.date <= budget.end_date]

        spent_amount = round(sum(t.amount for t in matching_expenses), 2)
        remaining_amount = round(budget.planned_amount - spent_amount, 2)

        if budget.planned_amount > 0:
            percentage_used = round((spent_amount / budget.planned_amount) * 100, 1)
        else:
            percentage_used = 0.0

        status: BudgetStatus
        if percentage_used < 80.0:
            status = "within"
        elif percentage_used <= 100.0:
            status = "warning"
        else:
            status = "exceeded"

        return cat_name, spent_amount, remaining_amount, percentage_used, status

    def _to_response(self, budget: BudgetInDb, user_id: str) -> BudgetResponse:
        (
            cat_name,
            spent,
            remaining,
            pct,
            status,
        ) = self._calculate_budget_metrics(budget, user_id)
        return BudgetResponse(
            id=budget.id,
            user_id=budget.user_id,
            category_id=budget.category_id,
            category_name=cat_name,
            planned_amount=budget.planned_amount,
            period=budget.period,
            start_date=budget.start_date,
            end_date=budget.end_date,
            spent_amount=spent,
            remaining_amount=remaining,
            percentage_used=pct,
            status=status,
            created_at=budget.created_at,
            updated_at=budget.updated_at,
        )

    def list_budgets(self, user_id: str) -> list[BudgetResponse]:
        budgets = self._budget_repo.list_by_user(user_id)
        return [self._to_response(b, user_id) for b in budgets]

    def get_budget(self, user_id: str, budget_id: str) -> BudgetResponse:
        budget = self._budget_repo.get_by_id(budget_id)
        if not budget or budget.user_id != user_id:
            raise BudgetNotFoundError(f"Budget {budget_id} not found")
        return self._to_response(budget, user_id)

    def create_budget(self, user_id: str, payload: BudgetCreate) -> BudgetResponse:
        category = self._cat_repo.get_by_id(payload.category_id)
        if not category or category.user_id != user_id:
            raise InvalidBudgetDataError("Selected category does not exist")
        if category.type != "expense":
            raise InvalidBudgetDataError("Budgets can only be created for expense categories")

        # Check for overlapping budget for the same category in the same month
        existing_budgets = self._budget_repo.list_by_user(user_id)
        month_prefix = payload.start_date[:7]
        for eb in existing_budgets:
            if eb.category_id == payload.category_id and eb.start_date.startswith(month_prefix):
                raise InvalidBudgetDataError(
                    f"A budget for '{category.name}' already exists for {month_prefix}"
                )

        budget_in_db = BudgetInDb(
            user_id=user_id,
            category_id=payload.category_id,
            planned_amount=payload.planned_amount,
            period=payload.period,
            start_date=payload.start_date,
            end_date=payload.end_date,
        )
        created = self._budget_repo.create(budget_in_db)
        return self._to_response(created, user_id)

    def update_budget(self, user_id: str, budget_id: str, payload: BudgetUpdate) -> BudgetResponse:
        budget = self._budget_repo.get_by_id(budget_id)
        if not budget or budget.user_id != user_id:
            raise BudgetNotFoundError(f"Budget {budget_id} not found")

        if payload.category_id is not None:
            category = self._cat_repo.get_by_id(payload.category_id)
            if not category or category.user_id != user_id:
                raise InvalidBudgetDataError("Selected category does not exist")
            if category.type != "expense":
                raise InvalidBudgetDataError("Budgets can only be created for expense categories")
            budget.category_id = payload.category_id

        if payload.planned_amount is not None:
            budget.planned_amount = payload.planned_amount
        if payload.period is not None:
            budget.period = payload.period
        if payload.start_date is not None:
            budget.start_date = payload.start_date
        if payload.end_date is not None:
            budget.end_date = payload.end_date

        budget.updated_at = datetime.now(UTC)
        updated = self._budget_repo.update(budget)
        return self._to_response(updated, user_id)

    def delete_budget(self, user_id: str, budget_id: str) -> None:
        budget = self._budget_repo.get_by_id(budget_id)
        if not budget or budget.user_id != user_id:
            raise BudgetNotFoundError(f"Budget {budget_id} not found")
        self._budget_repo.delete(budget_id)
