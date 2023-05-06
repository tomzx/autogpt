from datetime import timedelta

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
