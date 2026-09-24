from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_budget_service, get_current_user
from app.models.budget import BudgetCreate, BudgetResponse, BudgetUpdate
from app.models.user import UserInDb
from app.services.budget_service import (
    BudgetNotFoundError,
    BudgetService,
    InvalidBudgetDataError,
)

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.get("", response_model=list[BudgetResponse])
def list_budgets(
    current_user: UserInDb = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
) -> list[BudgetResponse]:
    return service.list_budgets(current_user.id)


@router.post("", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_budget(
    payload: BudgetCreate,
    current_user: UserInDb = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
) -> BudgetResponse:
    try:
        return service.create_budget(current_user.id, payload)
    except InvalidBudgetDataError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{budget_id}", response_model=BudgetResponse)
def get_budget(
    budget_id: str,
    current_user: UserInDb = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
) -> BudgetResponse:
    try:
        return service.get_budget(current_user.id, budget_id)
    except BudgetNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{budget_id}", response_model=BudgetResponse)
def update_budget(
    budget_id: str,
    payload: BudgetUpdate,
    current_user: UserInDb = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
) -> BudgetResponse:
    try:
        return service.update_budget(current_user.id, budget_id, payload)
    except BudgetNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidBudgetDataError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(
    budget_id: str,
    current_user: UserInDb = Depends(get_current_user),
    service: BudgetService = Depends(get_budget_service),
) -> None:
    try:
        service.delete_budget(current_user.id, budget_id)
    except BudgetNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
