from datetime import timedelta

import structlog

logger = structlog.getLogger(__name__)


class TimeBudget:
    def __init__(self) -> None:
        self.budget = None
        self.spent_budget = timedelta()

    def set_budget(self, budget: timedelta) -> None:
        self.budget = budget

    def is_budget_reached(self) -> bool:
        if self.budget is None:
            return False

        return self.spent_budget >= self.budget

    def update_spent_budget(self, cost: timedelta) -> None:
        self.spent_budget += cost

        budget = "∞"
        remaining_budget = "∞"
        if self.budget:
            budget = self.budget
            remaining_budget = budget - self.spent_budget
        logger.debug(
            "Time budget",
            budget=str(budget),
            spent_budget=str(self.spent_budget),
            remaining_budget=str(remaining_budget),
        )
