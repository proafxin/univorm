# mypy: disable_error_code="type-arg"

import os

import pytest
from bson.objectid import ObjectId
from polars import DataFrame
from pymongo import MongoClient

from univorm.db import NoSQLDatabaseDialect, async_nosql_client
from univorm.reader.nosql import find_in_collection, find_in_collection_async
from univorm.writer.nosql import insert_into_collection, insert_into_collection_async


@pytest.mark.asyncio
async def test_query_with_result(mongo_client: MongoClient) -> None:
    documents = [{"name": "test1"}, {"name": "test2"}]
    object_ids = insert_into_collection(documents=documents, client=mongo_client, dbname="test", collection_name="test")
    assert isinstance(object_ids, list)
    for object_id in object_ids:
        assert isinstance(object_id, ObjectId)

    df = find_in_collection(query={}, client=mongo_client, dbname="test", collection_name="test")
    assert isinstance(df, DataFrame)
    assert df.shape[0] > 0
    assert df.shape[1] > 1


@pytest.mark.asyncio
async def test_async_mongo_client_query() -> None:
    client = await async_nosql_client(
        user=os.environ["MONGO_INITDB_ROOT_USERNAME"],
        password=os.environ["MONGO_INITDB_ROOT_PASSWORD"],
        host=os.environ["MONGO_HOST"],
        port=int(os.environ["MONGO_PORT"]),
        dialect=NoSQLDatabaseDialect.MONGODB,
    )

    try:
        documents = [{"name": "test1"}, {"name": "test2"}]
        object_ids = await insert_into_collection_async(
            documents=documents, client=client, dbname="XXXX", collection_name="test"
        )
        assert isinstance(object_ids, list)
        for object_id in object_ids:
            assert isinstance(object_id, ObjectId)

        df = await find_in_collection_async(query={}, client=client, dbname="XXXX", collection_name="test")
        assert isinstance(df, DataFrame)
        assert df.shape[0] > 0
        assert df.shape[1] > 1
    finally:
        await client.close()
