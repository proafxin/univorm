import pytest
from polars import DataFrame
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine

from univorm.reader.sql import async_query_with_result, sync_query_with_result


@pytest.mark.asyncio
async def test_mysql_query(mysql_engine: AsyncEngine) -> None:
    query = "SHOW DATABASES"
    df = await async_query_with_result(query=query, engine=mysql_engine)
    assert isinstance(df, DataFrame)
    assert df.shape[0] > 4


@pytest.mark.asyncio
async def test_postgresql_query(postgres_engine: AsyncEngine) -> None:
    query = "SELECT * FROM pg_database"
    df = await async_query_with_result(query=query, engine=postgres_engine)
    assert isinstance(df, DataFrame)
    assert df.shape[0] >= 3


@pytest.mark.asyncio
async def test_sqlserver_query(sqlserver_engine: Engine) -> None:
    query = "SELECT * FROM master.sys.databases"
    df = sync_query_with_result(query=query, engine=sqlserver_engine)
    assert isinstance(df, DataFrame)
    assert df.shape[0] > 3
