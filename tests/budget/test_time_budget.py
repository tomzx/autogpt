from datetime import timedelta
import pytest

from autogpt.budget.time_budget import TimeBudget


def test_time_budget():
    budget = TimeBudget()
    budget.set_budget(timedelta(seconds=100))
    assert budget.is_budget_reached() == False
    budget.update_spent_budget(timedelta(seconds=10))
    assert budget.is_budget_reached() == False
    assert budget.spent_budget == timedelta(seconds=10)
    budget.update_spent_budget(timedelta(seconds=90))
    assert budget.is_budget_reached() == True
    assert budget.spent_budget == timedelta(seconds=100)


def test_time_budget_without_budget():
    budget = TimeBudget()
    assert budget.is_budget_reached() == False
    budget.update_spent_budget(timedelta(seconds=10))
    assert budget.is_budget_reached() == False
    assert budget.spent_budget == timedelta(seconds=10)


def test_time_budget_negative_budget():
    budget = TimeBudget()
    with pytest.raises(ValueError):
        budget.set_budget(timedelta(seconds=-1))


def test_time_budget_negative_cost():
    budget = TimeBudget()
    budget.set_budget(timedelta(seconds=10))
    with pytest.raises(ValueError):
        budget.update_spent_budget(timedelta(seconds=-5))
