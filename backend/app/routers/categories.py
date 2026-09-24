from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_category_service, get_current_user
from app.models.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.models.user import UserInDb
from app.services.category_service import (
    CategoryDuplicateError,
    CategoryInUseError,
    CategoryNotFoundError,
    CategoryService,
)

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryResponse])
def list_categories(
    current_user: UserInDb = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
) -> list[CategoryResponse]:
    return service.list_categories(current_user.id)


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    current_user: UserInDb = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
) -> CategoryResponse:
    try:
        return service.create_category(current_user.id, payload)
    except CategoryDuplicateError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: str,
    current_user: UserInDb = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
) -> CategoryResponse:
    try:
        return service.get_category(current_user.id, category_id)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: str,
    payload: CategoryUpdate,
    current_user: UserInDb = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
) -> CategoryResponse:
    try:
        return service.update_category(current_user.id, category_id, payload)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CategoryDuplicateError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: str,
    current_user: UserInDb = Depends(get_current_user),
    service: CategoryService = Depends(get_category_service),
) -> None:
    try:
        service.delete_category(current_user.id, category_id)
    except CategoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CategoryInUseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
