import pytest
from app.models.user import User
from app.models.expense import ExpenseItem
from app.services.dynamodb import (
    get_user_by_email,
    create_or_get_user,
    get_user_expenses,
    add_expense,
)
import uuid
from datetime import datetime, timezone
from decimal import Decimal

USER_EMAIL = "test@example.com"
USER_UUID = "abc-123-def-456"
EXPENSE_ID = "exp-uuid-001"


@pytest.fixture
def mock_users_table(mocker):
    mock = mocker.MagicMock()
    mocker.patch("app.services.dynamodb.get_table", return_value=mock)
    return mock


class TestGetUserByEmail:
    def test_given_no_user_return_none(self, mock_users_table):
        mock_users_table.get_item.return_value = {}
        assert get_user_by_email(USER_EMAIL) is None

    def test_given_existing_user_return_user(self, mock_users_table):
        # GIVEN
        mock_users_table.get_item.return_value = {
            "Item": {"uuid": USER_UUID, "email": USER_EMAIL}
        }
        
        # WHEN
        result = get_user_by_email(USER_EMAIL)
        
        # THEN
        mock_users_table.get_item.assert_called_once_with(Key={"email": USER_EMAIL})
        assert isinstance(result, User)
        assert result.uuid == USER_UUID


class TestCreateOrGetUser:
    def test_creates_new_user(self, mock_users_table):
        # GIVEN no existing user
        mock_users_table.get_item.return_value = {}
        
        # WHEN
        user = create_or_get_user(USER_EMAIL)
        
        # THEN
        assert isinstance(user, User)
        assert uuid.UUID(user.uuid)  # Validates that it's a proper UUID
        mock_users_table.put_item.assert_called_once_with(
            Item={"email": USER_EMAIL, "uuid": user.uuid})

    def test_returns_existing_user(self, mock_users_table):
        # GIVEN existing user
        mock_users_table.get_item.return_value = {
            "Item": {"uuid": USER_UUID, "email": USER_EMAIL}
        }

        # WHEN
        user = create_or_get_user(USER_EMAIL)

        # THEN
        assert user.uuid == USER_UUID
        mock_users_table.put_item.assert_not_called()


class TestExpenses:
    def test_get_expenses_empty(self, mock_users_table):
        mock_users_table.query.return_value = {"Items": []}
        assert get_user_expenses(USER_UUID) == []

    def test_get_expenses(self, mock_users_table):
        # GIVEN
        mock_users_table.query.return_value = {
            "Items": [{
                "id": EXPENSE_ID,
                "user_id": USER_UUID,
                "amount": 25.50,
                "description": "Lunch at cafe",
                "category": "Food",
                "expense_date": "2024-01-15T10:30:00Z",
            }]
        }
        
        # WHEN
        expenses = get_user_expenses(USER_UUID)
        
        # THEN
        assert len(expenses) == 1
        assert expenses[0].id == EXPENSE_ID
        assert expenses[0].amount == Decimal('25.50')
        assert expenses[0].description == "Lunch at cafe"
        assert expenses[0].category == "Food"
        assert expenses[0].expense_date == datetime(2024, 1, 15, 10, 30, tzinfo=timezone.utc)

    def test_add_expense(self, mock_users_table):
        mock_users_table.put_item.return_value = {}
        
        # WHEN
        expense = add_expense(
            user_id=USER_UUID,
            amount='25.5',
            description="Lunch at cafe",
            category="Food",
            expense_date="2024-01-15",
        )
        
        # THEN
        assert isinstance(expense, ExpenseItem)
        assert expense.user_id == USER_UUID
        assert expense.amount == 25.50
        assert expense.description == "Lunch at cafe"
        assert expense.category == "Food"
        mock_users_table.put_item.assert_called_once_with(
            Item={
                "id": expense.id,
                "user_id": USER_UUID,
                "amount": Decimal('25.50'),
                "description": "Lunch at cafe",
                "category": "Food",
                "expense_date": "2024-01-15T00:00:00",
            }
        )
