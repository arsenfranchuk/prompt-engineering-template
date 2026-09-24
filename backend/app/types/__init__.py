from typing import NewType

UserId = NewType("UserId", str)
CategoryId = NewType("CategoryId", str)
TransactionId = NewType("TransactionId", str)
BudgetId = NewType("BudgetId", str)

__all__ = ["UserId", "CategoryId", "TransactionId", "BudgetId"]
