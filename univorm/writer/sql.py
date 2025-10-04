from typing import Any

import polars as pl
from sqlalchemy import Boolean, Column, Date, DateTime, Float, Integer, MetaData, String, Table, Time
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine


async def async_write_dataframe(
    data: pl.DataFrame, table_name: str, engine: AsyncEngine, if_table_exists: str = "append", create_table: bool = True
) -> int:
    """Write DataFrame to SQL database asynchronously.

    Parameters
    ----------
    data : pl.DataFrame
        Polars DataFrame to write
    table_name : str
        Target table name
    engine : AsyncEngine
        SQLAlchemy async engine
    if_table_exists : str, default 'append'
        Action when table exists ('append', 'replace', 'fail')
    create_table : bool, default True
        Whether to create table if it doesn't exist

    Returns
    -------
    int
        Number of rows written
    """
    async with engine.begin() as conn:
        table_obj = _create_table_object(data, table_name, engine.dialect.name)

        if create_table:
            await conn.run_sync(table_obj.create, checkfirst=True)

        if if_table_exists == "replace":
            await conn.run_sync(table_obj.drop, checkfirst=True)
            await conn.run_sync(table_obj.create)

        values = data.to_dicts()
        if values:
            await conn.execute(table_obj.insert(), values)

        return len(data)


def sync_write_dataframe(
    data: pl.DataFrame, table_name: str, engine: Engine, if_table_exists: str = "append", create_table: bool = True
) -> int:
    """Write DataFrame to SQL database synchronously.

    Parameters
    ----------
    data : pl.DataFrame
        Polars DataFrame to write
    table_name : str
        Target table name
    engine : Engine
        SQLAlchemy sync engine
    if_table_exists : str, default 'append'
        Action when table exists ('append', 'replace', 'fail')
    create_table : bool, default True
        Whether to create table if it doesn't exist

    Returns
    -------
    int
        Number of rows written
    """
    with engine.begin() as conn:
        table_obj = _create_table_object(data, table_name, engine.dialect.name)

        if create_table:
            table_obj.create(conn, checkfirst=True)

        if if_table_exists == "replace":
            table_obj.drop(conn, checkfirst=True)
            table_obj.create(conn)

        values = data.to_dicts()
        if values:
            conn.execute(table_obj.insert(), values)

        return len(data)


def _create_table_object(data: pl.DataFrame, table_name: str, dialect: str) -> Table:
    """Create SQLAlchemy Table object based on DataFrame schema.

    Parameters
    ----------
    data : pl.DataFrame
        DataFrame with schema to replicate
    table_name : str
        Name of the table to create
    dialect : str
        SQL dialect name

    Returns
    -------
    Table
        SQLAlchemy Table object
    """
    metadata = MetaData()
    columns: list[Any] = []

    for column, dtype in data.schema.items():
        sql_type = _map_polars_to_sqlalchemy_type(dtype, dialect)
        columns.append(Column(column, sql_type))

    return Table(table_name, metadata, *columns)


def _map_polars_to_sqlalchemy_type(dtype: pl.DataType, dialect: str) -> Any:
    """Map Polars data types to SQLAlchemy types.

    Parameters
    ----------
    dtype : pl.DataType
        Polars data type to convert
    dialect : str
        SQL dialect name

    Returns
    -------
    Any
        SQLAlchemy type object
    """
    if dtype.is_integer():
        return Integer
    elif dtype.is_float():
        return Float
    elif dtype == pl.String:
        return String(255)  # MySQL requires length
    elif dtype == pl.Boolean:
        return Boolean
    elif dtype == pl.Date:
        return Date
    elif dtype == pl.Datetime:
        return DateTime
    elif dtype == pl.Time:
        return Time
    else:
        return String(255)  # Default for complex types
