from datetime import datetime, timedelta
from typing import Optional

from autogpt.budget.money_budget import MoneyBudget
from autogpt.budget.time_budget import TimeBudget


class Budget:
    """
    Composite budget class that manages all budget types.
    
    This class encapsulates different budget types (money, time, etc.)
    and provides a unified interface for budget management.
    """
    
    def __init__(self) -> None:
        self.money_budget = MoneyBudget()
        self.time_budget = TimeBudget()
    
    def set_money_budget(self, budget: Optional[float]) -> None:
        """Set the monetary budget limit."""
        self.money_budget.set_budget(budget)
    
    def set_time_budget(self, budget_seconds: Optional[int]) -> None:
        """Set the time budget limit in seconds."""
        if budget_seconds is not None:
            self.time_budget.set_budget(timedelta(seconds=budget_seconds))
    
    def update_money_spent(self, cost: float) -> None:
        """Update the amount of money spent."""
        self.money_budget.update_spent_budget(cost)
    
    def update_time_spent(self, elapsed_time: timedelta) -> None:
        """Update the amount of time spent."""
        self.time_budget.update_spent_budget(elapsed_time)
    
    def is_budget_reached(self) -> bool:
        """Check if any budget limit has been reached."""
        return self.money_budget.is_budget_reached() or self.time_budget.is_budget_reached()
    
    def get_money_budget_info(self) -> dict:
        """Get information about the money budget."""
        return {
            "budget": self.money_budget.budget,
            "spent": self.money_budget.spent_budget,
            "reached": self.money_budget.is_budget_reached()
        }
    
    def get_time_budget_info(self) -> dict:
        """Get information about the time budget."""
        return {
            "budget": self.time_budget.budget,
            "spent": self.time_budget.spent_budget,
            "reached": self.time_budget.is_budget_reached()
        }
