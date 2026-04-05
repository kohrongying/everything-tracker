import boto3
from boto3.dynamodb.conditions import Key

from app.core.config import settings


def get_dynamodb_resource():
    return boto3.resource("dynamodb", region_name=settings.aws_region)


def get_table():
    return get_dynamodb_resource().Table(settings.dynamodb_table)


def query_user_items(user_id: str, item_type: str):
    table = get_table()
    return table.query(
        KeyConditionExpression=Key("user_id").eq(user_id) & Key("item_type").eq(item_type)
    ).get("Items", [])
