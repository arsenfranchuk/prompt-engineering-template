from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.dependencies import get_auth_service, get_current_user
from app.models.user import (
    AuthResponse,
    UserChangePassword,
    UserInDb,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
    UserUpdateProfile,
)
from app.services.auth_service import (
    AuthenticationError,
    AuthService,
    UserAlreadyExistsError,
    UserNotFoundError,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(
    payload: UserRegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    try:
        return auth_service.register(payload)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=AuthResponse)
def login(
    payload: UserLoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> AuthResponse:
    try:
        return auth_service.login(payload)
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/logout")
def logout(
    authorization: Annotated[str | None, Header()] = None,
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, str]:
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split("Bearer ", 1)[1].strip()
        auth_service.logout(token)
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: UserInDb = Depends(get_current_user),
) -> UserResponse:
    return UserResponse.from_db(current_user)


@router.patch("/profile", response_model=UserResponse)
def update_profile(
    payload: UserUpdateProfile,
    current_user: UserInDb = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    try:
        return auth_service.update_profile(current_user.id, payload)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/change-password")
def change_password(
    payload: UserChangePassword,
    current_user: UserInDb = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, str]:
    try:
        auth_service.change_password(current_user.id, payload)
        return {"message": "Password updated successfully"}
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
