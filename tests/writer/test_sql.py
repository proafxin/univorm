from datetime import date, datetime, time

import polars as pl
import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine

from univorm.writer.sql import async_write_dataframe, sync_write_dataframe


@pytest.mark.asyncio
async def test_mysql_write(mysql_engine: AsyncEngine) -> None:
    data = pl.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"], "score": [95.5, 87.2, 92.1]})

    rows_written = await async_write_dataframe(
        data=data, table_name="test_users", engine=mysql_engine, if_table_exists="replace"
    )

    assert rows_written == 3


@pytest.mark.asyncio
async def test_postgresql_write(postgres_engine: AsyncEngine) -> None:
    data = pl.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"], "score": [95.5, 87.2, 92.1]})

    rows_written = await async_write_dataframe(
        data=data, table_name="test_users", engine=postgres_engine, if_table_exists="replace"
    )

    assert rows_written == 3


def test_sqlserver_write(sqlserver_engine: Engine) -> None:
    data = pl.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"], "score": [95.5, 87.2, 92.1]})

    rows_written = sync_write_dataframe(
        data=data, table_name="test_users", engine=sqlserver_engine, if_table_exists="replace"
    )

    assert rows_written == 3


@pytest.mark.asyncio
async def test_comprehensive_data_types(postgres_engine: AsyncEngine) -> None:
    data = pl.DataFrame(
        {
            "int8_col": pl.Series([1, 2, 3], dtype=pl.Int8),
            "int16_col": pl.Series([100, 200, 300], dtype=pl.Int16),
            "int32_col": pl.Series([1000, 2000, 3000], dtype=pl.Int32),
            "int64_col": pl.Series([10000, 20000, 30000], dtype=pl.Int64),
            "uint8_col": pl.Series([1, 2, 3], dtype=pl.UInt8),
            "uint16_col": pl.Series([100, 200, 300], dtype=pl.UInt16),
            "uint32_col": pl.Series([1000, 2000, 3000], dtype=pl.UInt32),
            "uint64_col": pl.Series([10000, 20000, 30000], dtype=pl.UInt64),
            "float32_col": pl.Series([1.1, 2.2, 3.3], dtype=pl.Float32),
            "float64_col": pl.Series([1.11, 2.22, 3.33], dtype=pl.Float64),
            "string_col": ["Alice", "Bob", "Charlie"],
            "bool_col": [True, False, True],
            "date_col": [date(2023, 1, 1), date(2023, 1, 2), date(2023, 1, 3)],
            "datetime_col": [datetime(2023, 1, 1, 12, 0), datetime(2023, 1, 2, 13, 0), datetime(2023, 1, 3, 14, 0)],
            "time_col": [time(12, 0), time(13, 0), time(14, 0)],
            "list_col": ["[1, 2]", "[3, 4]", "[5, 6]"],
            "struct_col": ["{\"a\": 1}", "{\"b\": 2}", "{\"c\": 3}"],
        }
    )

    rows_written = await async_write_dataframe(
        data=data, table_name="test_types", engine=postgres_engine, if_table_exists="replace"
    )

    assert rows_written == 3
