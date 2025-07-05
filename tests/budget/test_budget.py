from datetime import timedelta

from autogpt.budget.budget import Budget


def test_composite_budget_initialization():
    """Test that the composite budget initializes with both money and time budgets."""
    budget = Budget()
    
    # Should have both budget types
    assert budget.money_budget is not None
    assert budget.time_budget is not None
    
    # Should not be reached by default
    assert budget.is_budget_reached() == False


def test_money_budget_operations():
    """Test money budget operations through the composite budget."""
    budget = Budget()
    
    # Set money budget
    budget.set_money_budget(100.0)
    assert budget.get_money_budget_info()["budget"] == 100.0
    assert budget.get_money_budget_info()["spent"] == 0.0
    assert budget.get_money_budget_info()["reached"] == False
    
    # Update money spent
    budget.update_money_spent(50.0)
    assert budget.get_money_budget_info()["spent"] == 50.0
    assert budget.is_budget_reached() == False
    
    # Exceed money budget
    budget.update_money_spent(60.0)  # Total 110.0
    assert budget.get_money_budget_info()["reached"] == True
    assert budget.is_budget_reached() == True


def test_time_budget_operations():
    """Test time budget operations through the composite budget."""
    budget = Budget()
    
    # Set time budget
    budget.set_time_budget(100)  # 100 seconds
    assert budget.get_time_budget_info()["budget"] == timedelta(seconds=100)
    assert budget.get_time_budget_info()["spent"] == timedelta(seconds=0)
    assert budget.get_time_budget_info()["reached"] == False
    
    # Update time spent
    budget.update_time_spent(timedelta(seconds=50))
    assert budget.get_time_budget_info()["spent"] == timedelta(seconds=50)
    assert budget.is_budget_reached() == False
    
    # Exceed time budget
    budget.update_time_spent(timedelta(seconds=60))  # Total 110 seconds
    assert budget.get_time_budget_info()["reached"] == True
    assert budget.is_budget_reached() == True


def test_combined_budget_operations():
    """Test that either budget type can cause termination."""
    budget = Budget()
    
    # Set both budgets
    budget.set_money_budget(100.0)
    budget.set_time_budget(100)
    
    # Neither exceeded
    budget.update_money_spent(50.0)
    budget.update_time_spent(timedelta(seconds=50))
    assert budget.is_budget_reached() == False
    
    # Only time budget exceeded
    budget.update_time_spent(timedelta(seconds=60))  # Total 110 seconds
    assert budget.is_budget_reached() == True


def test_budget_without_limits():
    """Test that budget doesn't terminate when no limits are set."""
    budget = Budget()
    
    # No budgets set
    budget.update_money_spent(1000.0)
    budget.update_time_spent(timedelta(hours=1))
    assert budget.is_budget_reached() == False


def test_none_budget_values():
    """Test that None budget values are handled correctly."""
    budget = Budget()
    
    # Setting None should not set a budget
    budget.set_money_budget(None)
    budget.set_time_budget(None)
    
    assert budget.get_money_budget_info()["budget"] is None
    assert budget.get_time_budget_info()["budget"] is None
    assert budget.is_budget_reached() == False