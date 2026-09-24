from datetime import datetime, timezone
import calendar

from app.models.dashboard import (
    BudgetSummary,
    CategoryIncomeItem,
    CategorySpendingItem,
    DashboardSummaryResponse,
    MonthlyTrendItem,
)
from app.models.transaction import TransactionResponse
from app.repositories.budget_repository import BudgetRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.transaction_repository import TransactionRepository


class DashboardService:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        category_repository: CategoryRepository,
        budget_repository: BudgetRepository,
    ) -> None:
        self._tx_repo = transaction_repository
        self._cat_repo = category_repository
        self._budget_repo = budget_repository

    def _get_category_map(self, user_id: str) -> dict[str, str]:
        cats = self._cat_repo.list_by_user(user_id)
        return {c.id: c.name for c in cats}

    def _get_period_bounds(self, period: str) -> tuple[str | None, str | None]:
        now = datetime.now(timezone.utc)
        year = now.year
        month = now.month

        if period == "current_month":
            start_date = f"{year:04d}-{month:02d}-01"
            _, last_day = calendar.monthrange(year, month)
            end_date = f"{year:04d}-{month:02d}-{last_day:02d}"
            return start_date, end_date
        elif period == "previous_month":
            prev_year = year if month > 1 else year - 1
            prev_month = month - 1 if month > 1 else 12
            start_date = f"{prev_year:04d}-{prev_month:02d}-01"
            _, last_day = calendar.monthrange(prev_year, prev_month)
            end_date = f"{prev_year:04d}-{prev_month:02d}-{last_day:02d}"
            return start_date, end_date
        elif period == "current_year":
            start_date = f"{year:04d}-01-01"
            end_date = f"{year:04d}-12-31"
            return start_date, end_date
        else:  # "all"
            return None, None

    def get_summary(self, user_id: str, period: str = "current_month") -> DashboardSummaryResponse:
        all_txs = self._tx_repo.list_by_user(user_id)
        cat_map = self._get_category_map(user_id)

        # Cumulative balance
        total_income_all_time = sum(t.amount for t in all_txs if t.type == "income")
        total_expense_all_time = sum(t.amount for t in all_txs if t.type == "expense")
        current_balance = round(total_income_all_time - total_expense_all_time, 2)

        # Filter by selected period
        start_date, end_date = self._get_period_bounds(period)
        period_txs = all_txs
        if start_date:
            period_txs = [t for t in period_txs if t.date >= start_date]
        if end_date:
            period_txs = [t for t in period_txs if t.date <= end_date]

        period_income = round(sum(t.amount for t in period_txs if t.type == "income"), 2)
        period_expenses = round(sum(t.amount for t in period_txs if t.type == "expense"), 2)
        period_net = round(period_income - period_expenses, 2)

        savings_rate = 0.0
        if period_income > 0 and period_net > 0:
            savings_rate = round((period_net / period_income) * 100, 1)

        # Spending by category
        expense_by_cat: dict[str, float] = {}
        for t in period_txs:
            if t.type == "expense":
                expense_by_cat[t.category_id] = round(
                    expense_by_cat.get(t.category_id, 0.0) + t.amount, 2
                )

        spending_by_category: list[CategorySpendingItem] = []
        for cat_id, amt in sorted(expense_by_cat.items(), key=lambda x: x[1], reverse=True):
            pct = round((amt / period_expenses * 100), 1) if period_expenses > 0 else 0.0
            spending_by_category.append(
                CategorySpendingItem(
                    category_id=cat_id,
                    category_name=cat_map.get(cat_id, "Unknown"),
                    amount=amt,
                    percentage=pct,
                )
            )

        # Income by category
        income_by_cat: dict[str, float] = {}
        for t in period_txs:
            if t.type == "income":
                income_by_cat[t.category_id] = round(
                    income_by_cat.get(t.category_id, 0.0) + t.amount, 2
                )

        income_by_category: list[CategoryIncomeItem] = []
        for cat_id, amt in sorted(income_by_cat.items(), key=lambda x: x[1], reverse=True):
            pct = round((amt / period_income * 100), 1) if period_income > 0 else 0.0
            income_by_category.append(
                CategoryIncomeItem(
                    category_id=cat_id,
                    category_name=cat_map.get(cat_id, "Unknown"),
                    amount=amt,
                    percentage=pct,
                )
            )

        # Active Budgets Summary
        user_budgets = self._budget_repo.list_by_user(user_id)
        now = datetime.now(timezone.utc)
        current_month_prefix = f"{now.year:04d}-{now.month:02d}"
        active_budgets = [
            b
            for b in user_budgets
            if b.start_date.startswith(current_month_prefix)
            or (b.start_date <= f"{now.year:04d}-{now.month:02d}-{now.day:02d}" and (not b.end_date or b.end_date >= f"{now.year:04d}-{now.month:02d}-{now.day:02d}"))
        ]

        total_planned = round(sum(b.planned_amount for b in active_budgets), 2)
        total_spent = 0.0
        for b in active_budgets:
            matching = [
                t
                for t in all_txs
                if t.category_id == b.category_id
                and t.type == "expense"
                and t.date.startswith(current_month_prefix)
            ]
            total_spent += sum(t.amount for t in matching)
        total_spent = round(total_spent, 2)
        total_remaining = round(total_planned - total_spent, 2)
        budget_pct = round((total_spent / total_planned * 100), 1) if total_planned > 0 else 0.0

        budget_summary = BudgetSummary(
            total_planned=total_planned,
            total_spent=total_spent,
            total_remaining=total_remaining,
            percentage_used=budget_pct,
            active_count=len(active_budgets),
        )

        # Recent transactions (last 6)
        sorted_txs = sorted(all_txs, key=lambda t: (t.date, t.created_at), reverse=True)
        recent_txs = [
            TransactionResponse.from_db(t, cat_map.get(t.category_id, "Unknown"))
            for t in sorted_txs[:6]
        ]

        # Monthly trends (past 6 months)
        monthly_trends: list[MonthlyTrendItem] = []
        for i in range(5, -1, -1):
            m = now.month - i
            y = now.year
            while m <= 0:
                m += 12
                y -= 1
            month_key = f"{y:04d}-{m:02d}"
            label = datetime(y, m, 1).strftime("%b %Y")
            m_txs = [t for t in all_txs if t.date.startswith(month_key)]
            m_inc = round(sum(t.amount for t in m_txs if t.type == "income"), 2)
            m_exp = round(sum(t.amount for t in m_txs if t.type == "expense"), 2)
            monthly_trends.append(
                MonthlyTrendItem(
                    month=month_key,
                    label=label,
                    income=m_inc,
                    expense=m_exp,
                    net=round(m_inc - m_exp, 2),
                )
            )

        return DashboardSummaryResponse(
            current_balance=current_balance,
            period=period,
            period_income=period_income,
            period_expenses=period_expenses,
            period_net=period_net,
            savings_rate=savings_rate,
            spending_by_category=spending_by_category,
            income_by_category=income_by_category,
            budget_summary=budget_summary,
            recent_transactions=recent_txs,
            monthly_trend=monthly_trends,
        )
