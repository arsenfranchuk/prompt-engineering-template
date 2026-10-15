from pydantic import BaseModel

from app.models.transaction import TransactionResponse


class CategorySpendingItem(BaseModel):
    category_id: str
    category_name: str
    amount: float
    percentage: float


class CategoryIncomeItem(BaseModel):
    category_id: str
    category_name: str
    amount: float
    percentage: float


class BudgetSummary(BaseModel):
    total_planned: float
    total_spent: float
    total_remaining: float
    percentage_used: float
    active_count: int


class MonthlyTrendItem(BaseModel):
    month: str  # YYYY-MM
    label: str  # e.g. "Sep 2026"
    income: float
    expense: float
    net: float


class DashboardSummaryResponse(BaseModel):
    current_balance: float
    period: str
    period_income: float
    period_expenses: float
    period_net: float
    savings_rate: float
    spending_by_category: list[CategorySpendingItem]
    income_by_category: list[CategoryIncomeItem]
    budget_summary: BudgetSummary
    recent_transactions: list[TransactionResponse]
    monthly_trend: list[MonthlyTrendItem]
