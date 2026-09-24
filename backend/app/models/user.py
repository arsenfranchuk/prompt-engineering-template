from datetime import datetime, timezone
import re
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


EMAIL_REGEX = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$")


class UserRegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=6, max_length=100)
    password_confirm: str = Field(min_length=6, max_length=100)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        s = v.strip()
        if len(s) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return s

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        s = v.strip().lower()
        if not EMAIL_REGEX.match(s):
            raise ValueError("Invalid email format")
        return s

    @field_validator("password_confirm")
    @classmethod
    def validate_passwords_match(cls, v: str, info) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v


class UserLoginRequest(BaseModel):
    identifier: str = Field(min_length=1, description="Username or email")
    password: str = Field(min_length=1)

    @field_validator("identifier")
    @classmethod
    def clean_identifier(cls, v: str) -> str:
        return v.strip()


class UserUpdateProfile(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    email: str | None = Field(default=None, min_length=5, max_length=100)

    @field_validator("username")
    @classmethod
    def clean_username(cls, v: str | None) -> str | None:
        if v is None:
            return None
        s = v.strip()
        if len(s) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return s

    @field_validator("email")
    @classmethod
    def clean_email(cls, v: str | None) -> str | None:
        if v is None:
            return None
        s = v.strip().lower()
        if not EMAIL_REGEX.match(s):
            raise ValueError("Invalid email format")
        return s


class UserChangePassword(BaseModel):
    current_password: str = Field(min_length=1)
    new_password: str = Field(min_length=6, max_length=100)
    new_password_confirm: str = Field(min_length=6, max_length=100)

    @field_validator("new_password_confirm")
    @classmethod
    def validate_new_passwords_match(cls, v: str, info) -> str:
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("New passwords do not match")
        return v


class UserInDb(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    username: str
    email: str
    password_hash: str
    salt: str
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)


class SessionInDb(BaseModel):
    token: str
    user_id: str
    created_at: datetime = Field(default_factory=_utc_now)


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime

    @classmethod
    def from_db(cls, user: UserInDb) -> "UserResponse":
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
        )


class AuthResponse(BaseModel):
    token: str
    user: UserResponse
