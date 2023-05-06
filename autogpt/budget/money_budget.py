import math
from typing import Optional

import structlog

logger = structlog.getLogger(__name__)


class MoneyBudget:
    def __init__(self) -> None:
        self.budget = None
        self.spent_budget = 0

    def set_budget(self, budget: Optional[float]) -> None:
        if budget is not None and budget < 0:
            raise ValueError("Budget must be >= 0.")

        self.budget = budget
        logger.debug("Budget set", budget=self.budget)

    def is_budget_reached(self) -> bool:
        if self.budget is None:
            return False

        return self.spent_budget >= self.budget

    def update_spent_budget(self, cost: float) -> None:
        self.spent_budget += cost
        budget = self.budget or math.inf
        logger.debug(
            "Money budget",
            budget=round(budget, 4),
            spent_budget=round(self.spent_budget, 4),
            remaining_budget=round(budget - self.spent_budget, 4),
        )
