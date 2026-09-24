from datetime import datetime, timezone
from app.models.user import (
    AuthResponse,
    UserChangePassword,
    UserInDb,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
    UserUpdateProfile,
)
from app.repositories.category_repository import CategoryRepository
from app.repositories.user_repository import UserRepository
from app.utils.security import hash_password, verify_password


class AuthenticationError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        category_repository: CategoryRepository,
    ) -> None:
        self._user_repo = user_repository
        self._cat_repo = category_repository

    def register(self, payload: UserRegisterRequest) -> AuthResponse:
        # Check uniqueness
        if self._user_repo.get_by_username(payload.username):
            raise UserAlreadyExistsError("Username is already taken")
        if self._user_repo.get_by_email(payload.email):
            raise UserAlreadyExistsError("Email is already registered")

        pw_hash, salt = hash_password(payload.password)
        user_in_db = UserInDb(
            username=payload.username,
            email=payload.email,
            password_hash=pw_hash,
            salt=salt,
        )
        created_user = self._user_repo.create(user_in_db)

        # Seed default income and expense categories for new user
        self._cat_repo.seed_defaults_for_user(created_user.id)

        # Create session
        session = self._user_repo.create_session(created_user.id)

        return AuthResponse(
            token=session.token,
            user=UserResponse.from_db(created_user),
        )

    def login(self, payload: UserLoginRequest) -> AuthResponse:
        user = self._user_repo.get_by_email(payload.identifier)
        if not user:
            user = self._user_repo.get_by_username(payload.identifier)

        if not user or not verify_password(payload.password, user.password_hash, user.salt):
            raise AuthenticationError("Invalid username/email or password")

        session = self._user_repo.create_session(user.id)
        return AuthResponse(
            token=session.token,
            user=UserResponse.from_db(user),
        )

    def logout(self, token: str) -> None:
        self._user_repo.delete_session(token)

    def authenticate_token(self, token: str) -> UserInDb:
        session = self._user_repo.get_session(token)
        if not session:
            raise AuthenticationError("Invalid or expired session")
        user = self._user_repo.get_by_id(session.user_id)
        if not user:
            raise AuthenticationError("User not found")
        return user

    def update_profile(self, user_id: str, payload: UserUpdateProfile) -> UserResponse:
        user = self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")

        if payload.username and payload.username.lower() != user.username.lower():
            existing = self._user_repo.get_by_username(payload.username)
            if existing and existing.id != user_id:
                raise UserAlreadyExistsError("Username is already taken")
            user.username = payload.username

        if payload.email and payload.email.lower() != user.email.lower():
            existing = self._user_repo.get_by_email(payload.email)
            if existing and existing.id != user_id:
                raise UserAlreadyExistsError("Email is already registered")
            user.email = payload.email

        user.updated_at = datetime.now(timezone.utc)
        updated = self._user_repo.update(user)
        return UserResponse.from_db(updated)

    def change_password(self, user_id: str, payload: UserChangePassword) -> None:
        user = self._user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")

        if not verify_password(payload.current_password, user.password_hash, user.salt):
            raise AuthenticationError("Current password is incorrect")

        new_hash, new_salt = hash_password(payload.new_password)
        user.password_hash = new_hash
        user.salt = new_salt
        user.updated_at = datetime.now(timezone.utc)
        self._user_repo.update(user)
