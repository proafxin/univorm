import pytest

from univorm.db import (
    NOSQL_DRIVERS,
    SQL_DRIVERS,
    NoSQLDatabaseDialect,
    NoSQLDatabaseDriver,
    SQLDatabaseDialect,
    SQLDatabaseDriver,
)


@pytest.mark.asyncio
async def test_dialects_drivers() -> None:
    for dialect in SQLDatabaseDialect:
        assert dialect.value in SQL_DRIVERS
        assert SQL_DRIVERS[dialect.value] in SQLDatabaseDriver

    assert NoSQLDatabaseDialect.MONGODB.value in NOSQL_DRIVERS
    assert NOSQL_DRIVERS[NoSQLDatabaseDialect.MONGODB.value] in NoSQLDatabaseDriver
