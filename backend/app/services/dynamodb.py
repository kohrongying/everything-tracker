import uuid
from decimal import Decimal
from typing import Optional
from datetime import datetime

import boto3
from aws_lambda_powertools.logging import Logger

from app.core.config import settings
from app.models.user import User
from app.models.expense import ExpenseItem

logger = Logger(service="everything-tracker")


def get_dynamodb_resource():
    """Get DynamoDB resource with local or AWS configuration."""
    if settings.use_local_dynamodb:
        return boto3.resource(
            "dynamodb",
            endpoint_url=settings.local_dynamodb_endpoint,
            region_name="us-east-1",  # Local DynamoDB doesn't care about region
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
        )
    else:
        return boto3.resource("dynamodb", region_name=settings.aws_region)


def get_table(table_name: str):
    return get_dynamodb_resource().Table(table_name)


# Users Service
def get_user_by_email(email: str) -> Optional[User]:
    """Fetch user from DynamoDB by email."""
    try:
        table = get_table(settings.users_table_name)

        response = table.get_item(Key={"email": email})
        item = response.get("Item")

        if not item:
            logger.info(
                "User not found", extra={"email": email, "event": "user_not_found"}
            )
            return None

        logger.info(
            "User found",
            extra={"email": email, "uuid": item.get("uuid"), "event": "user_found"},
        )
        return User(uuid=item["uuid"])

    except Exception as e:
        logger.exception(
            "Error fetching user from DynamoDB", extra={"email": email, "error": str(e)}
        )
        return None


def create_or_get_user(email: str) -> User:
    """Create or update user in DynamoDB."""
    try:
        table = get_table(settings.users_table_name)

        # Check if user exists
        response = table.get_item(Key={"email": email})
        existing_user = response.get("Item")

        if existing_user:
            user_uuid = existing_user["uuid"]
            logger.info(
                "User already exists",
                extra={"email": email, "uuid": user_uuid, "event": "user_exists"},
            )
        else:
            user_uuid = str(uuid.uuid4())
            table.put_item(Item={"email": email, "uuid": user_uuid})
            logger.info(
                "User created",
                extra={"email": email, "uuid": user_uuid, "event": "user_created"},
            )

        return User(uuid=user_uuid)

    except Exception as e:
        logger.exception(
            "Error creating/updating user in DynamoDB",
            extra={"email": email, "error": str(e)},
        )
        raise


# Expenses Service

USER_EXPENSE_INDEX_NAME = "user_id_index"

def get_user_expenses(user_id: str) -> list[ExpenseItem]:
    """Fetch all expenses for a user from DynamoDB using GSI."""
    try:
        table = get_table(settings.expenses_table_name)

        response = table.query(
            IndexName=USER_EXPENSE_INDEX_NAME,
            KeyConditionExpression="user_id = :user_id",
            ExpressionAttributeValues={":user_id": user_id},
        )

        items = response.get("Items", [])
        logger.info(
            "Expenses fetched",
            extra={
                "user_id": user_id,
                "count": len(items),
                "event": "expenses_fetched",
            },
        )

        return [
            ExpenseItem(
                id=item["id"],
                user_id=item["user_id"],
                amount=Decimal(str(item["amount"])),
                description=item["description"],
                category=item.get("category"),
                expense_date=datetime.fromisoformat(item["expense_date"]),
            )
            for item in items
        ]

    except Exception as e:
        logger.exception(
            "Error fetching expenses from DynamoDB",
            extra={"user_id": user_id, "error": str(e)},
        )
        return []


def add_expense(
    user_id: str,
    amount: str,
    description: str,
    category: str,
    expense_date: str,
) -> ExpenseItem:
    """Add a new expense to DynamoDB."""
    try:
        expense_id = str(uuid.uuid4())
        table = get_table(settings.expenses_table_name)

        item = {
            "id": expense_id,
            "user_id": user_id,
            "amount": Decimal(f"{float(amount):.2f}"),
            "description": description,
            "category": category,
            "expense_date": datetime.fromisoformat(expense_date).isoformat(),
        }

        table.put_item(Item=item)

        logger.info(
            "Expense added",
            extra={
                "user_id": user_id,
                "expense_id": expense_id,
                "amount": amount,
                "event": "expense_added",
            },
        )

        return ExpenseItem(
            id=expense_id,
            user_id=user_id,
            amount=amount,
            description=description,
            category=category,
            expense_date=expense_date,
        )

    except Exception as e:
        logger.exception(
            "Error adding expense to DynamoDB",
            extra={"user_id": user_id, "error": str(e)},
        )
        raise
