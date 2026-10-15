from pathlib import Path

from app.models.budget import BudgetInDb
from app.utils.json_store import read_list_file, write_list_file


class BudgetRepository:
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def list_all(self) -> list[BudgetInDb]:
        return read_list_file(self._file_path, BudgetInDb)

    def list_by_user(self, user_id: str) -> list[BudgetInDb]:
        return [b for b in self.list_all() if b.user_id == user_id]

    def get_by_id(self, budget_id: str) -> BudgetInDb | None:
        return next((b for b in self.list_all() if b.id == budget_id), None)

    def count_by_category(self, category_id: str) -> int:
        return sum(1 for b in self.list_all() if b.category_id == category_id)

    def create(self, budget: BudgetInDb) -> BudgetInDb:
        budgets = self.list_all()
        budgets.append(budget)
        write_list_file(self._file_path, budgets)
        return budget

    def update(self, budget: BudgetInDb) -> BudgetInDb:
        budgets = self.list_all()
        for idx, b in enumerate(budgets):
            if b.id == budget.id:
                budgets[idx] = budget
                write_list_file(self._file_path, budgets)
                return budget
        raise KeyError(f"Budget {budget.id} not found")

    def delete(self, budget_id: str) -> bool:
        budgets = self.list_all()
        filtered = [b for b in budgets if b.id != budget_id]
        if len(filtered) == len(budgets):
            return False
        write_list_file(self._file_path, filtered)
        return True
