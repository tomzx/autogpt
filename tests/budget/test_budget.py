from datetime import timedelta

from autogpt.budget.budget import Budget, BudgetManager


def test_base_budget_class_exists():
    """Test that the base Budget class still exists and can be used for inheritance."""
    # Should be able to create a Budget instance
    budget = Budget()
    assert budget is not None
    
    # Should be able to inherit from Budget
    class CustomBudget(Budget):
        def __init__(self):
            super().__init__()
            self.custom_property = "test"
    
    custom_budget = CustomBudget()
    assert custom_budget.custom_property == "test"


def test_budget_manager_initialization():
    """Test that the budget manager initializes with both money and time budgets."""
    budget_manager = BudgetManager()
    
    # Should have both budget types
    assert budget_manager.money_budget is not None
    assert budget_manager.time_budget is not None
    
    # Should not be reached by default
    assert budget_manager.is_budget_reached() == False


def test_money_budget_operations():
    """Test money budget operations through the budget manager."""
    budget_manager = BudgetManager()
    
    # Set money budget
    budget_manager.set_money_budget(100.0)
    assert budget_manager.get_money_budget_info()["budget"] == 100.0
    assert budget_manager.get_money_budget_info()["spent"] == 0.0
    assert budget_manager.get_money_budget_info()["reached"] == False
    
    # Update money spent
    budget_manager.update_money_spent(50.0)
    assert budget_manager.get_money_budget_info()["spent"] == 50.0
    assert budget_manager.is_budget_reached() == False
    
    # Exceed money budget
    budget_manager.update_money_spent(60.0)  # Total 110.0
    assert budget_manager.get_money_budget_info()["reached"] == True
    assert budget_manager.is_budget_reached() == True


def test_time_budget_operations():
    """Test time budget operations through the budget manager."""
    budget_manager = BudgetManager()
    
    # Set time budget
    budget_manager.set_time_budget(100)  # 100 seconds
    assert budget_manager.get_time_budget_info()["budget"] == timedelta(seconds=100)
    assert budget_manager.get_time_budget_info()["spent"] == timedelta(seconds=0)
    assert budget_manager.get_time_budget_info()["reached"] == False
    
    # Update time spent
    budget_manager.update_time_spent(timedelta(seconds=50))
    assert budget_manager.get_time_budget_info()["spent"] == timedelta(seconds=50)
    assert budget_manager.is_budget_reached() == False
    
    # Exceed time budget
    budget_manager.update_time_spent(timedelta(seconds=60))  # Total 110 seconds
    assert budget_manager.get_time_budget_info()["reached"] == True
    assert budget_manager.is_budget_reached() == True


def test_combined_budget_operations():
    """Test that either budget type can cause termination."""
    budget_manager = BudgetManager()
    
    # Set both budgets
    budget_manager.set_money_budget(100.0)
    budget_manager.set_time_budget(100)
    
    # Neither exceeded
    budget_manager.update_money_spent(50.0)
    budget_manager.update_time_spent(timedelta(seconds=50))
    assert budget_manager.is_budget_reached() == False
    
    # Only time budget exceeded
    budget_manager.update_time_spent(timedelta(seconds=60))  # Total 110 seconds
    assert budget_manager.is_budget_reached() == True


def test_budget_without_limits():
    """Test that budget doesn't terminate when no limits are set."""
    budget_manager = BudgetManager()
    
    # No budgets set
    budget_manager.update_money_spent(1000.0)
    budget_manager.update_time_spent(timedelta(hours=1))
    assert budget_manager.is_budget_reached() == False


def test_none_budget_values():
    """Test that None budget values are handled correctly."""
    budget_manager = BudgetManager()
    
    # Setting None should not set a budget
    budget_manager.set_money_budget(None)
    budget_manager.set_time_budget(None)
    
    assert budget_manager.get_money_budget_info()["budget"] is None
    assert budget_manager.get_time_budget_info()["budget"] is None
    assert budget_manager.is_budget_reached() == False