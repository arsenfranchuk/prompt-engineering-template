from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


def _utc_now() -> datetime:
    return datetime.now(UTC)


BudgetPeriod = Literal["monthly", "custom"]
BudgetStatus = Literal["within", "warning", "exceeded"]


class BudgetBase(BaseModel):
    category_id: str = Field(min_length=1)
    planned_amount: float = Field(gt=0, description="Planned budget amount must be positive")
    period: BudgetPeriod = "monthly"
    start_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    end_date: str | None = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")

    @field_validator("planned_amount")
    @classmethod
    def round_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Planned amount must be greater than zero")
        return round(v, 2)


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    category_id: str | None = None
    planned_amount: float | None = Field(default=None, gt=0)
    period: BudgetPeriod | None = None
    start_date: str | None = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    end_date: str | None = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")

    @field_validator("planned_amount")
    @classmethod
    def round_amount(cls, v: float | None) -> float | None:
        if v is None:
            return None
        if v <= 0:
            raise ValueError("Planned amount must be greater than zero")
        return round(v, 2)


class BudgetInDb(BudgetBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)


class BudgetResponse(BudgetBase):
    id: str
    user_id: str
    category_name: str = ""
    spent_amount: float = 0.0
    remaining_amount: float = 0.0
    percentage_used: float = 0.0
    status: BudgetStatus = "within"
    created_at: datetime
    updated_at: datetime
