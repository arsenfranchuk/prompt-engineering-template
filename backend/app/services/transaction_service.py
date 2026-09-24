from datetime import datetime, timezone
from app.models.transaction import (
    TransactionCreate,
    TransactionInDb,
    TransactionResponse,
    TransactionUpdate,
)
from app.repositories.category_repository import CategoryRepository
from app.repositories.transaction_repository import TransactionRepository


class TransactionNotFoundError(Exception):
    pass


class InvalidTransactionDataError(Exception):
    pass


class TransactionService:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        category_repository: CategoryRepository,
    ) -> None:
        self._tx_repo = transaction_repository
        self._cat_repo = category_repository

    def _get_category_map(self, user_id: str) -> dict[str, str]:
        cats = self._cat_repo.list_by_user(user_id)
        return {c.id: c.name for c in cats}

    def list_transactions(
        self,
        user_id: str,
        type: str | None = None,
        category_id: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        search: str | None = None,
        sort_by: str = "date",  # "date" | "amount"
        sort_order: str = "desc",  # "desc" | "asc"
    ) -> list[TransactionResponse]:
        items = self._tx_repo.list_by_user(user_id)
        cat_map = self._get_category_map(user_id)

        # Filtering
        if type and type in ("income", "expense"):
            items = [t for t in items if t.type == type]
        if category_id:
            items = [t for t in items if t.category_id == category_id]
        if start_date:
            items = [t for t in items if t.date >= start_date]
        if end_date:
            items = [t for t in items if t.date <= end_date]
        if search:
            query = search.strip().lower()
            items = [
                t
                for t in items
                if query in t.description.lower() or query in cat_map.get(t.category_id, "").lower()
            ]

        # Sorting
        reverse = sort_order.lower() == "desc"
        if sort_by == "amount":
            items = sorted(items, key=lambda t: t.amount, reverse=reverse)
        else:
            # Default sort by date, secondary by created_at
            items = sorted(items, key=lambda t: (t.date, t.created_at), reverse=reverse)

        return [TransactionResponse.from_db(t, cat_map.get(t.category_id, "Unknown")) for t in items]

    def get_transaction(self, user_id: str, tx_id: str) -> TransactionResponse:
        tx = self._tx_repo.get_by_id(tx_id)
        if not tx or tx.user_id != user_id:
            raise TransactionNotFoundError(f"Transaction {tx_id} not found")
        cat_map = self._get_category_map(user_id)
        return TransactionResponse.from_db(tx, cat_map.get(tx.category_id, "Unknown"))

    def create_transaction(self, user_id: str, payload: TransactionCreate) -> TransactionResponse:
        # Validate category
        category = self._cat_repo.get_by_id(payload.category_id)
        if not category or category.user_id != user_id:
            raise InvalidTransactionDataError("Selected category does not exist")
        if category.type != payload.type:
            raise InvalidTransactionDataError(
                f"Category '{category.name}' is a {category.type} category, but transaction is '{payload.type}'"
            )

        tx_in_db = TransactionInDb(
            user_id=user_id,
            type=payload.type,
            amount=payload.amount,
            category_id=payload.category_id,
            date=payload.date,
            description=payload.description,
        )
        created = self._tx_repo.create(tx_in_db)
        return TransactionResponse.from_db(created, category.name)

    def update_transaction(
        self, user_id: str, tx_id: str, payload: TransactionUpdate
    ) -> TransactionResponse:
        tx = self._tx_repo.get_by_id(tx_id)
        if not tx or tx.user_id != user_id:
            raise TransactionNotFoundError(f"Transaction {tx_id} not found")

        target_type = payload.type or tx.type
        target_category_id = payload.category_id or tx.category_id

        category = self._cat_repo.get_by_id(target_category_id)
        if not category or category.user_id != user_id:
            raise InvalidTransactionDataError("Selected category does not exist")
        if category.type != target_type:
            raise InvalidTransactionDataError(
                f"Category '{category.name}' is a {category.type} category, but transaction is '{target_type}'"
            )

        if payload.type is not None:
            tx.type = payload.type
        if payload.amount is not None:
            tx.amount = payload.amount
        if payload.category_id is not None:
            tx.category_id = payload.category_id
        if payload.date is not None:
            tx.date = payload.date
        if payload.description is not None:
            tx.description = payload.description

        tx.updated_at = datetime.now(timezone.utc)
        updated = self._tx_repo.update(tx)
        return TransactionResponse.from_db(updated, category.name)

    def delete_transaction(self, user_id: str, tx_id: str) -> None:
        tx = self._tx_repo.get_by_id(tx_id)
        if not tx or tx.user_id != user_id:
            raise TransactionNotFoundError(f"Transaction {tx_id} not found")
        self._tx_repo.delete(tx_id)
