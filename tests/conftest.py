# mypy: disable_error_code="type-arg"

import os
from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from dotenv import load_dotenv
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

load_dotenv()


@pytest.fixture(scope="session")
def mongo_client() -> Generator[MongoClient, None, None]:
    client = nosql_client(
        user=os.environ["MONGO_INITDB_ROOT_USERNAME"],
        password=os.environ["MONGO_INITDB_ROOT_PASSWORD"],
        host=os.environ["MONGO_HOST"],
        port=int(os.environ["MONGO_PORT"]),
        dialect=NoSQLDatabaseDialect.MONGODB,
    )
    yield client
    client.close()


@pytest_asyncio.fixture(scope="function")
async def mysql_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = await async_sql_engine(
        user="root",
        password=os.environ["MYSQL_ROOT_PASSWORD"],
        port=int(os.environ["MYSQL_TCP_PORT"]),
        dialect=SQLDatabaseDialect.MYSQL,
        host=os.environ["MYSQL_HOST"],
        dbname=os.environ["MYSQL_DATABASE"],
    )

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def postgres_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = await async_sql_engine(
        user=os.environ["PGUSER"],
        password=os.environ["POSTGRES_PASSWORD"],
        port=int(os.environ["POSTGRESQL_PORT"]),
        dialect=SQLDatabaseDialect.POSTGRESQL,
        host=os.environ["POSTGRESQL_HOST"],
        dbname=os.environ["POSTGRES_DB"],
    )

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def sqlserver_engine() -> AsyncGenerator[Engine, None]:
    engine = sync_sql_engine(
        user=os.environ["SQLSERVER_USER"],
        password=os.environ["SA_PASSWORD"],
        port=int(os.environ["SQLSERVER_PORT"]),
        dialect=SQLDatabaseDialect.SQLSERVER,
        host=os.environ["SQLSERVER_HOST"],
        dbname="master",
    )

    yield engine
    engine.dispose()
