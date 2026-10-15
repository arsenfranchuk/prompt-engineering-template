import re
from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


def _utc_now() -> datetime:
    return datetime.now(UTC)


DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TransactionType = Literal["income", "expense"]


class TransactionBase(BaseModel):
    type: TransactionType
    amount: float = Field(gt=0, description="Amount must be positive")
    category_id: str = Field(min_length=1)
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$", description="Date in YYYY-MM-DD format")
    description: str = Field(default="", max_length=500)

    @field_validator("amount")
    @classmethod
    def round_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Amount must be greater than zero")
        return round(v, 2)

    @field_validator("description")
    @classmethod
    def clean_description(cls, v: str) -> str:
        return v.strip()


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    type: TransactionType | None = None
    amount: float | None = Field(default=None, gt=0)
    category_id: str | None = None
    date: str | None = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    description: str | None = Field(default=None, max_length=500)

    @field_validator("amount")
    @classmethod
    def round_amount(cls, v: float | None) -> float | None:
        if v is None:
            return None
        if v <= 0:
            raise ValueError("Amount must be greater than zero")
        return round(v, 2)

    @field_validator("description")
    @classmethod
    def clean_description(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return v.strip()


class TransactionInDb(TransactionBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)


class TransactionResponse(TransactionBase):
    id: str
    user_id: str
    category_name: str = ""
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_db(cls, tx: TransactionInDb, category_name: str = "") -> "TransactionResponse":
        return cls(
            id=tx.id,
            user_id=tx.user_id,
            type=tx.type,
            amount=tx.amount,
            category_id=tx.category_id,
            category_name=category_name,
            date=tx.date,
            description=tx.description,
            created_at=tx.created_at,
            updated_at=tx.updated_at,
        )
