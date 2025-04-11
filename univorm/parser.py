from datetime import datetime
from typing import Any, Sequence

import pandas as pd
import polars as pl
from pydantic import BaseModel, TypeAdapter, create_model


class Base(BaseModel):
    pass


async def camel_case(name: str) -> str:
    delimiters = []
    for character in name:
        if not character.isalnum():
            delimiters.append(character)

    for delimiter in delimiters:
        name = " ".join(name.split(delimiter))

    tokens = name.split()

    return "".join(token.lower().capitalize() for token in tokens)


async def deserialize_pydantic_objects(models: Sequence[BaseModel]) -> pl.DataFrame:
    data = [model.model_dump() for model in models]

    return pl.DataFrame(data=data)


async def flatten(data: pd.DataFrame | pl.DataFrame, depth: int) -> pl.DataFrame:
    if isinstance(data, pd.DataFrame):
        data = pl.from_pandas(data=data)

    return pl.json_normalize(data=data.to_dicts(), max_level=depth)


async def _serialize_data(model_name: str, data: list[dict[Any, Any]], fields: dict[str, Any]) -> list[BaseModel]:
    Model = create_model(model_name, **fields)

    ta = TypeAdapter(list[Model])  # type: ignore[valid-type]

    return ta.validate_python(data)


async def _serialize_table_polars(table_name: str, data: pl.DataFrame) -> list[BaseModel]:
    fields: dict[str, Any] = {}
    field_type: Any

    for column, dtype in data.schema.items():
        non_nulls = data.select(pl.col(column)).drop_nulls()
        cell = non_nulls.row(0)[0]

        if dtype.is_integer():
            field_type = int
        elif dtype.is_float():
            field_type = float
        elif dtype == pl.String:
            field_type = str
        elif dtype == pl.Datetime:
            field_type = datetime
        elif dtype == pl.Struct:
            field_type = dict[Any, Any]
        elif dtype == pl.List:
            if isinstance(cell[0], int):
                field_type = list[int]
            elif isinstance(cell[0], float):
                field_type = list[float]
            elif isinstance(cell[0], str):
                field_type = list[str]
            elif isinstance(cell[0], datetime):
                field_type = list[datetime]
            else:
                field_type = list[Any]

        if non_nulls.shape[0] < data.shape[0]:
            fields[column] = (field_type | None, ...)
        else:
            fields[column] = (field_type, ...)

    return await _serialize_data(model_name=table_name, data=data.to_dicts(), fields=fields)


async def serialize_table(table_name: str, data: pd.DataFrame | pl.DataFrame) -> list[BaseModel]:
    table_name = await camel_case(name=table_name)
    if isinstance(data, pd.DataFrame):
        data = pl.from_pandas(data=data)

    return await _serialize_table_polars(table_name=table_name, data=data)
