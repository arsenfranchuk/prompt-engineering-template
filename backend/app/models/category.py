from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


CategoryType = Literal["income", "expense"]


class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    type: CategoryType

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Category name cannot be empty")
        return s


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=50)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Category name cannot be empty")
        return s


class CategoryInDb(CategoryBase):
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    is_default: bool = False
    created_at: datetime = Field(default_factory=_utc_now)


class CategoryResponse(CategoryBase):
    id: str
    user_id: str
    is_default: bool
    created_at: datetime

    @classmethod
    def from_db(cls, cat: CategoryInDb) -> "CategoryResponse":
        return cls(
            id=cat.id,
            user_id=cat.user_id,
            name=cat.name,
            type=cat.type,
            is_default=cat.is_default,
            created_at=cat.created_at,
        )
