from datetime import timedelta
from typing import Optional

import structlog

logger = structlog.getLogger(__name__)


class TimeBudget:
    """Track and enforce a time budget expressed as a ``timedelta``.

    The class mirrors the behaviour of :class:`autogpt.budget.money_budget.MoneyBudget` but
    operates on time instead of money.
    """

    def __init__(self) -> None:
        # ``None`` means *no* budget (infinite time)
        self.budget: Optional[timedelta] = None
        self.spent_budget: timedelta = timedelta()

    def set_budget(self, budget: Optional[timedelta]) -> None:
        """Set the maximum time that can be spent.

        Args:
            budget: The maximum time allowed. ``None`` means unlimited.
        """

        if budget is not None and budget < timedelta():
            raise ValueError("Budget must be >= 0.")

        self.budget = budget
        logger.debug("Budget set", budget=str(self.budget))

    def is_budget_reached(self) -> bool:
        """Return ``True`` when the spent time equals or exceeds the budget."""

        if self.budget is None:
            return False

        return self.spent_budget >= self.budget

    def update_spent_budget(self, cost: timedelta) -> None:
        """Add *cost* to the spent budget and log the current state."""

        if cost < timedelta():
            raise ValueError("Cost must be >= 0.")

        self.spent_budget += cost

        budget_display = str(self.budget) if self.budget is not None else "∞"
        remaining_display = "∞"
        if self.budget is not None:
            remaining_display = str(self.budget - self.spent_budget)

        logger.debug(
            "Time budget",
            budget=budget_display,
            spent_budget=str(self.spent_budget),
            remaining_budget=remaining_display,
        )
