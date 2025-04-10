# mypy: disable_error_code="type-arg"

from typing import Any

from bson.objectid import ObjectId
from pymongo import MongoClient


def insert_into_collection(
    documents: list[dict[str, Any]],
    client: MongoClient,
    dbname: str,
    collection_name: str,
) -> list[ObjectId]:
    db = client[dbname]
    collection = db[collection_name]
    result = collection.insert_many(documents=documents)

    return result.inserted_ids
