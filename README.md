# Xin

A pydantic powered universal ORM wrapper for databases.

This is a python package I created to reuse some functionalities I have had to implement in multiple jobs. For some reason, there aren't any ORM wrappers we can just plug and play. This should help in that area to some extent. I am trying to make it as generalized as possible but data storage services that require paid access may never be part of this package.

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/proafxin/xin/develop.svg)](https://results.pre-commit.ci/latest/github/proafxin/xin/develop)
[![Build, Test and Publish](https://github.com/proafxin/xin/actions/workflows/cicd.yaml/badge.svg)](https://github.com/proafxin/xin/actions/workflows/cicd.yaml)
[![codecov](https://codecov.io/gh/proafxin/xin/graph/badge.svg?token=p2cOg8tQMb)](https://codecov.io/gh/proafxin/xin)
[![Documentation Status](https://readthedocs.org/projects/xin/badge/?version=latest)](https://xin.readthedocs.io/en/latest/?badge=latest)

## Features

* Execute queries on a database.
* Read a database table as a dataframe.
* Write a dataframe to a database table (still under development).
* Flatten and normalize a dataframe with nested structure.
* Serialize a dataframe as a list of pydantic models.
* Deserialize a list of pydantic models as a dataframe.

The primary backend for parsing dataframes is [polars](https://pola.rs/) due to it's superior [performance](https://pola.rs/_astro/perf-illustration.jHjw6PiD_165TDG.svg). `Xin` supports pandas dataframes as well, however, they are internally converted to polars dataframes first to not compromise performance.

The backend  for interacting with SQL databases is [sqlalchemy](https://www.sqlalchemy.org/) because it supports async features and is the de-facto standard for communicating with SQL databases.

## Databases Supported

* MySQL
* PostgreSQL
* SQL Server
* Mongodb

## Async Drivers Supported

`Xin` is async first. It means that if an async driver is available for a database dialect, it will leverage the async driver for better performance when  applicable. SQL Server driver PyMSSQL does not have an async variation yet.

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
