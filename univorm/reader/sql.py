from polars import DataFrame
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine


async def async_query_with_result(query: str, engine: AsyncEngine) -> DataFrame:
    async with engine.connect() as conn:
        result = await conn.execute(text(query))
        data = result.fetchall()

        return DataFrame(data=data)


def sync_query_with_result(query: str, engine: Engine) -> DataFrame:
    with engine.connect() as conn:
        result = conn.execute(text(query))
        data = result.fetchall()

        return DataFrame(data=data)
