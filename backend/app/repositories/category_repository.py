from pathlib import Path

from app.models.category import CategoryInDb
from app.utils.json_store import read_list_file, write_list_file

DEFAULT_INCOME_CATEGORIES = [
    "Salary",
    "Freelance & Side Gigs",
    "Investments & Dividends",
    "Gifts & Grants",
    "Other Income",
]

DEFAULT_EXPENSE_CATEGORIES = [
    "Food & Groceries",
    "Housing & Rent",
    "Utilities & Bills",
    "Transportation",
    "Entertainment & Leisure",
    "Shopping & Personal",
    "Healthcare & Medical",
    "Education & Courses",
    "Other Expenses",
]


class CategoryRepository:
    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def list_all(self) -> list[CategoryInDb]:
        return read_list_file(self._file_path, CategoryInDb)

    def list_by_user(self, user_id: str) -> list[CategoryInDb]:
        return [c for c in self.list_all() if c.user_id == user_id]

    def get_by_id(self, category_id: str) -> CategoryInDb | None:
        return next((c for c in self.list_all() if c.id == category_id), None)

    def create(self, category: CategoryInDb) -> CategoryInDb:
        categories = self.list_all()
        categories.append(category)
        write_list_file(self._file_path, categories)
        return category

    def update(self, category: CategoryInDb) -> CategoryInDb:
        categories = self.list_all()
        for idx, c in enumerate(categories):
            if c.id == category.id:
                categories[idx] = category
                write_list_file(self._file_path, categories)
                return category
        raise KeyError(f"Category {category.id} not found")

    def delete(self, category_id: str) -> bool:
        categories = self.list_all()
        filtered = [c for c in categories if c.id != category_id]
        if len(filtered) == len(categories):
            return False
        write_list_file(self._file_path, filtered)
        return True

    def seed_defaults_for_user(self, user_id: str) -> list[CategoryInDb]:
        categories = self.list_all()
        user_categories = [c for c in categories if c.user_id == user_id]
        if user_categories:
            return user_categories

        seeded: list[CategoryInDb] = []
        for name in DEFAULT_INCOME_CATEGORIES:
            seeded.append(CategoryInDb(user_id=user_id, name=name, type="income", is_default=True))
        for name in DEFAULT_EXPENSE_CATEGORIES:
            seeded.append(CategoryInDb(user_id=user_id, name=name, type="expense", is_default=True))

        categories.extend(seeded)
        write_list_file(self._file_path, categories)
        return seeded
