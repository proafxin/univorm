# mypy: disable_error_code="type-arg"

from typing import Any

from bson.objectid import ObjectId
from pymongo import AsyncMongoClient, MongoClient


def insert_into_collection(
    documents: list[dict[str, Any]], client: MongoClient, dbname: str, collection_name: str
) -> list[ObjectId]:
    db = client[dbname]
    collection = db[collection_name]
    result = collection.insert_many(documents=documents)

    return result.inserted_ids


async def insert_into_collection_async(
    documents: list[dict[str, Any]], client: AsyncMongoClient, dbname: str, collection_name: str
) -> list[ObjectId]:
    db = client[dbname]
    collection = db[collection_name]
    result = await collection.insert_many(documents=documents)

    return result.inserted_ids
