from autogpt.budget.money_budget import MoneyBudget


def test_money_budget():
    budget = MoneyBudget()
    budget.set_budget(100)
    assert budget.is_budget_reached() == False
    budget.update_spent_budget(10)
    assert budget.is_budget_reached() == False
    assert budget.spent_budget == 10
    budget.update_spent_budget(90)
    assert budget.is_budget_reached() == True
    assert budget.spent_budget == 100


def test_money_budget_without_budget():
    budget = MoneyBudget()
    assert budget.is_budget_reached() == False
    budget.update_spent_budget(10)
    assert budget.is_budget_reached() == False
    assert budget.spent_budget == 10
