from pathlib import Path
from app.models.transaction import TransactionInDb
from app.utils.json_store import read_list_file, write_list_file


class TransactionRepository:
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def list_all(self) -> list[TransactionInDb]:
        return read_list_file(self._file_path, TransactionInDb)

    def list_by_user(self, user_id: str) -> list[TransactionInDb]:
        return [t for t in self.list_all() if t.user_id == user_id]

    def get_by_id(self, tx_id: str) -> TransactionInDb | None:
        return next((t for t in self.list_all() if t.id == tx_id), None)

    def count_by_category(self, category_id: str) -> int:
        return sum(1 for t in self.list_all() if t.category_id == category_id)

    def create(self, transaction: TransactionInDb) -> TransactionInDb:
        transactions = self.list_all()
        transactions.append(transaction)
        write_list_file(self._file_path, transactions)
        return transaction

    def update(self, transaction: TransactionInDb) -> TransactionInDb:
        transactions = self.list_all()
        for idx, t in enumerate(transactions):
            if t.id == transaction.id:
                transactions[idx] = transaction
                write_list_file(self._file_path, transactions)
                return transaction
        raise KeyError(f"Transaction {transaction.id} not found")

    def delete(self, tx_id: str) -> bool:
        transactions = self.list_all()
        filtered = [t for t in transactions if t.id != tx_id]
        if len(filtered) == len(transactions):
            return False
        write_list_file(self._file_path, filtered)
        return True
