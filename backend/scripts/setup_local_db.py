#!/usr/bin/env python3
"""
Setup script for local DynamoDB tables.
Run this after starting the local DynamoDB container.
"""

import boto3
import sys
from pathlib import Path

# Point to backend/ so app imports resolve correctly
sys.path.insert(0, str(Path(__file__).parent.parent)) 

from app.core.config import settings
from app.services.dynamodb import create_or_get_user
from app.auth.oauth import generate_access_token

TEST_USER_EMAIL = "test@example.com"

def create_tables():
    """Create DynamoDB tables for local development."""

    # Configure for local DynamoDB
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=settings.local_dynamodb_endpoint,
        region_name="us-east-1",
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
    )

    # Create users table
    try:
        users_table = dynamodb.create_table(
            TableName=settings.users_table_name,
            KeySchema=[
                {"AttributeName": "email", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "email", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST"
        )
        print(f"✅ Created users table: {settings.users_table_name}")
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print(f"ℹ️  Users table {settings.users_table_name} already exists")

    # Create expenses table
    try:
        expenses_table = dynamodb.create_table(
            TableName=settings.expenses_table_name,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},
                {"AttributeName": "user_id", "AttributeType": "S"},
                {"AttributeName": "expense_date", "AttributeType": "S"}
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "user_id_index",
                    "KeySchema": [
                        {"AttributeName": "user_id", "KeyType": "HASH"},
                        {"AttributeName": "expense_date", "KeyType": "RANGE"}
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                }
            ],
            BillingMode="PAY_PER_REQUEST"
        )
        print(f"✅ Created expenses table: {settings.expenses_table_name}")
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print(f"ℹ️  Expenses table {settings.expenses_table_name} already exists")

    print("\n🎉 Local DynamoDB tables setup complete!")

def create_test_user():
    user = create_or_get_user(TEST_USER_EMAIL)
    token = generate_access_token(user.uuid)
    print(f"\n👤 Test User")
    print(f"   Email : {TEST_USER_EMAIL}")
    print(f"   UUID  : {user.uuid}")
    print(f"\n🔑 Access Token:\n   {token}")
    print(f"\n📋 curl example:")
    print(f"   curl -H 'Authorization: Bearer {token}' http://localhost:8000/expenses")

if __name__ == "__main__":
    create_tables()
    create_test_user()