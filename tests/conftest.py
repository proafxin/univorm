# mypy: disable_error_code="type-arg"

import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from pymongo import MongoClient
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine

from univorm.db import (
    NoSQLDatabaseDialect,
    SQLDatabaseDialect,
    async_sql_engine,
    nosql_client,
    sync_sql_engine,
)


@pytest.fixture(scope="session")
def mongo_client() -> Generator[MongoClient, None, None]:
    client = nosql_client(
        user=os.environ["MONGO_USER"],
        password=os.environ["MONGO_PASSWORD"],
        host=os.environ["MONGO_HOST"],
        dialect=NoSQLDatabaseDialect.MONGODB,
    )
    yield client
    client.close()


@pytest_asyncio.fixture(scope="session")
async def mysql_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = await async_sql_engine(
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        port=int(os.environ["MYSQL_PORT"]),
        dialect=SQLDatabaseDialect.MYSQL,
        host="localhost",
        dbname=os.environ["MYSQL_DBNAME"],
    )

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def postgres_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = await async_sql_engine(
        user=os.environ["POSTGRESQL_USER"],
        password=os.environ["POSTGRESQL_PASSWORD"],
        port=int(os.environ["POSTGRESQL_PORT"]),
        dialect=SQLDatabaseDialect.POSTGRESQL,
        host="localhost",
        dbname="postgres",
    )

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def sqlserver_engine() -> AsyncGenerator[Engine, None]:
    engine = sync_sql_engine(
        user=os.environ["SQLSERVER_USER"],
        password=os.environ["SQLSERVER_PASSWORD"],
        port=int(os.environ["SQLSERVER_PORT"]),
        dialect=SQLDatabaseDialect.SQLSERVER,
        host="localhost",
        dbname="master",
    )

    yield engine
    engine.dispose()
