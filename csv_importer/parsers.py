import databpy as db
import polars as pl
import numpy as np


def polars_df_to_bob(df: pl.DataFrame, name: str) -> db.BlenderObject:
    vertices = np.zeros((len(df), 3), dtype=np.float32)
    bob = db.create_bob(vertices, name=name)

    for col in df.columns:
        col_dtype = df[col].dtype
        if col_dtype in [pl.Utf8]:
            continue
        data = df[col].to_numpy()
        bob.store_named_attribute(data, col)

    return bob
