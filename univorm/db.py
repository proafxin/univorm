# mypy: disable_error_code="type-arg"

from enum import Enum

from pymongo import AsyncMongoClient, MongoClient
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


class SQLDatabaseDialect(str, Enum):
    """SQL database flavors."""

    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    SQLSERVER = "mssql"


class SQLDatabaseDriver(str, Enum):
    AIOMYSQL = "aiomysql"
    ASYNCPG = "asyncpg"
    PYMSSQL = "pymssql"


class NoSQLDatabaseDialect(str, Enum):
    MONGODB = "mongodb"
    SCYLLADB = "scylladb"
    CASSANDRA = "cassandra"


class NoSQLDatabaseDriver(Enum):
    MOTOR = "motor"


SQL_DRIVERS = {
    SQLDatabaseDialect.MYSQL.value: SQLDatabaseDriver.AIOMYSQL.value,
    SQLDatabaseDialect.POSTGRESQL.value: SQLDatabaseDriver.ASYNCPG.value,
    SQLDatabaseDialect.SQLSERVER.value: SQLDatabaseDriver.PYMSSQL.value,
}

NOSQL_DRIVERS = {NoSQLDatabaseDialect.MONGODB.value: NoSQLDatabaseDriver.MOTOR.value}


def create_connection_string(
    user: str,
    password: str,
    port: int,
    dialect: SQLDatabaseDialect,
    host: str,
    dbname: str,
) -> str:
    dbinfo = dialect.value
    if dbinfo in SQL_DRIVERS:
        dbinfo = f"{dbinfo}+{SQL_DRIVERS[dialect]}"

    connection_string = f"{dbinfo}://{user}:{password}@{host}:{port}/{dbname}"

    return connection_string


async def async_sql_engine(
    user: str,
    password: str,
    port: int,
    dialect: SQLDatabaseDialect,
    host: str,
    dbname: str,
) -> AsyncEngine:
    url = create_connection_string(
        user=user,
        password=password,
        port=port,
        dialect=dialect,
        host=host,
        dbname=dbname,
    )
    return create_async_engine(url=url)


def sync_sql_engine(
    user: str,
    password: str,
    port: int,
    dialect: SQLDatabaseDialect,
    host: str,
    dbname: str,
) -> Engine:
    url = create_connection_string(
        user=user,
        password=password,
        port=port,
        dialect=dialect,
        host=host,
        dbname=dbname,
    )

    return create_engine(url=url)


def nosql_client(user: str, password: str, dialect: NoSQLDatabaseDialect, host: str) -> MongoClient:
    driver = "mongodb"
    # if host != "localhost" and host != "127.0.0.1":
    driver += "+srv"
    connection_string = f"{driver}://{user}:{password}@{host}/retryWrites=true&w=majority"
    client: MongoClient = MongoClient(connection_string)

    return client


async def async_nosql_client(user: str, password: str, dialect: NoSQLDatabaseDialect, host: str) -> AsyncMongoClient:
    driver = "mongodb"
    # if host != "localhost" and host != "127.0.0.1":
    driver += "+srv"
    connection_string = f"{driver}://{user}:{password}@{host}/retryWrites=true&w=majority"
    client: AsyncMongoClient = AsyncMongoClient(connection_string)

    return client
