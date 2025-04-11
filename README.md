# Univorm

A pydantic powered universal ORM wrapper for databases.

This is a python package I created to reuse some functionalities I have had to implement in multiple jobs. For some reason, there aren't any ORM wrappers we can just plug and play. This should help in that area to some extent. I am trying to make it as generalized as possible but data storage services that require paid access may never be part of this package.

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/proafxin/xin/develop.svg)](https://results.pre-commit.ci/latest/github/proafxin/xin/develop)
[![Build, Test and Publish](https://github.com/proafxin/xin/actions/workflows/cicd.yaml/badge.svg?branch=develop)](https://github.com/proafxin/xin/actions/workflows/cicd.yaml)
[![codecov](https://codecov.io/gh/proafxin/xin/graph/badge.svg?token=p2cOg8tQMb)](https://codecov.io/gh/proafxin/xin)
[![Documentation Status](https://readthedocs.org/projects/xin/badge/?version=latest)](https://xin.readthedocs.io/en/latest/?badge=latest)

## Usage

### Serialize a dataframe (Pandas/Polars)

```python
now = datetime.now()
data1 = {
    "n": "xin",
    "id": 200,
    "f": ["a", "b", "c"],
    "c": now,
    "b": 20.0,
    "d": {"a": 1},
    "e": [[1]],
}
data2 = {
    "n": "xin",
    "id": 200,
    "f": ["d", "e", "f"],
    "c": now,
    "b": None,
    "d": {"a": 1},
    "e": [[2]],
}

pydantic_objects = await serialize_table(table_name="some_table", data=pd.DataFrame(data=[data1, data2]))
```

### Deserialize a Pydantic Model

```python
class DummyModel(BaseModel):
    x: int
    y: float

models = [DummyModel(x=1, y=2.0), DummyModel(x=10, y=-1.9)]
df = await deserialize_pydantic_objects(models=models)
```

### Flatten NoSQL data to SQL (Pandas/Polars)

```python
data = [
    {
        "id": 1,
        "name": "Cole Volk",
        "fitness": {"height": 130, "weight": 60},
    },
    {"name": "Mark Reg", "fitness": {"height": 130, "weight": 60}},
    {
        "id": 2,
        "name": "Faye Raker",
        "fitness": {"height": 130, "weight": 60},
    },
]

df_pandas = pd.DataFrame(data=data)
df_polars = pl.DataFrame(data=data)
flat_df = await flatten(data=df_pandas, depth=0)
flat_df = await flatten(data=df_polars, depth=0)
flat_df = await flatten(data=df_polars, depth=1)
```

### Connect to a mongodb client

```python
def mongo_client() -> Generator[MongoClient, None, None]:
    client = nosql_client(
        user=os.environ["MONGO_USER"],
        password=os.environ["MONGO_PASSWORD"],
        host=os.environ["MONGO_HOST"],
        dialect=NoSQLDatabaseDialect.MONGODB,
    )
    yield client
    client.close()
```

### Run query on Mongo

```python
documents = [{"name": "test1"}, {"name": "test2"}]
object_ids = insert_into_collection(
    documents=documents, client=mongo_client, dbname="test", collection_name="test"
)

df = find_in_collection(
    query={}, client=mongo_client, dbname="test", collection_name="test"
)
```

### Query a MySQL engine

Create the engine:

```python
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
```

Make query:

```python
query = "SHOW DATABASES"
df = await async_query_with_result(query=query, engine=mysql_engine)
```

### Query a PostgreSQL engine

Create the engine:

```python
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
```

Make query:

```python
query = "SELECT * FROM pg_database"
df = await async_query_with_result(query=query, engine=postgres_engine)
```

### Create a SQL Server Engine

Create the engine:

```python
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
```

Make query:

```python
query = "SELECT * FROM master.sys.databases"
df = sync_query_with_result(query=query, engine=sqlserver_engine)
```

The primary backend for parsing dataframes is [polars](https://pola.rs/) due to it's superior [performance](https://pola.rs/_astro/perf-illustration.jHjw6PiD_165TDG.svg). `univorm` supports pandas dataframes as well, however, they are internally converted to polars dataframes first to not compromise performance.

The backend  for interacting with SQL databases is [sqlalchemy](https://www.sqlalchemy.org/) because it supports async features and is the de-facto standard for communicating with SQL databases.

## Databases Supported

* MySQL
* PostgreSQL
* SQL Server
* Mongodb

## Async Drivers Supported

`univorm` is async first. It means that if an async driver is available for a database dialect, it will leverage the async driver for better performance when  applicable. SQL Server driver PyMSSQL does not have an async variation yet.

* [PyMongo](https://pymongo.readthedocs.io/en/stable/index.html) for Mongodb. Currently async support is in beta but since PyMongo is natively supporting async features, it's safer to use it rather than a third party package like [Motor](https://motor.readthedocs.io/en/stable/index.html).
* [Asyncpg](https://magicstack.github.io/asyncpg/current/) for PostgreSQL.
* [AioMySQL](https://aiomysql.readthedocs.io/en/stable/) for MySQL.

## Plan for Future Database Support

* [Couchbase Capella](https://www.couchbase.com/products/capella/)
* [Scylladb](https://www.scylladb.com/)
* [Apache Cassandra](https://cassandra.apache.org/_/index.html)

## Test Locally

Have `docker compose`, [tox](https://tox.wiki/en/4.25.0/) and [uv](https://docs.astral.sh/uv/getting-started/installation/) installed. Then run `docker compose up -d`. Create the environment

```bash
uv venv
uv sync --dev --extra formatting --extra docs
uv lock
```

Then run `tox -p`
