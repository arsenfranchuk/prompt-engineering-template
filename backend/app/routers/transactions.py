from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_current_user, get_transaction_service
from app.models.transaction import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)
from app.models.user import UserInDb
from app.services.transaction_service import (
    InvalidTransactionDataError,
    TransactionNotFoundError,
    TransactionService,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[TransactionResponse])
def list_transactions(
    type: str | None = Query(default=None, description="Filter by type: income or expense"),
    category_id: str | None = Query(default=None, description="Filter by category ID"),
    start_date: str | None = Query(default=None, description="Filter transactions from date (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="Filter transactions to date (YYYY-MM-DD)"),
    search: str | None = Query(default=None, description="Search keyword in description or category"),
    sort_by: str = Query(default="date", description="Sort by field: date or amount"),
    sort_order: str = Query(default="desc", description="Sort order: desc or asc"),
    current_user: UserInDb = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
) -> list[TransactionResponse]:
    return service.list_transactions(
        user_id=current_user.id,
        type=type,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionCreate,
    current_user: UserInDb = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    try:
        return service.create_transaction(current_user.id, payload)
    except InvalidTransactionDataError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{tx_id}", response_model=TransactionResponse)
def get_transaction(
    tx_id: str,
    current_user: UserInDb = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    try:
        return service.get_transaction(current_user.id, tx_id)
    except TransactionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{tx_id}", response_model=TransactionResponse)
def update_transaction(
    tx_id: str,
    payload: TransactionUpdate,
    current_user: UserInDb = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
) -> TransactionResponse:
    try:
        return service.update_transaction(current_user.id, tx_id, payload)
    except TransactionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidTransactionDataError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{tx_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    tx_id: str,
    current_user: UserInDb = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
) -> None:
    try:
        service.delete_transaction(current_user.id, tx_id)
    except TransactionNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
