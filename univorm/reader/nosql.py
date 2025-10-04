# mypy: disable_error_code="type-arg"

from typing import Any

from polars import DataFrame
from pymongo import AsyncMongoClient, MongoClient


def find_in_collection(query: dict[str, Any], client: MongoClient, dbname: str, collection_name: str) -> DataFrame:
    db = client[dbname]

    collection = db[collection_name]
    documents = collection.find(query)

    return DataFrame(data=[document for document in documents])


async def find_in_collection_async(
    query: dict[str, Any], client: AsyncMongoClient, dbname: str, collection_name: str
) -> DataFrame:
    db = client[dbname]

    collection = db[collection_name]
    documents = collection.find(query)

    return DataFrame(data=[document async for document in documents])
