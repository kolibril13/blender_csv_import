import databpy as db
import polars as pl
import numpy as np
import bpy


def polars_df_to_bob(df: pl.DataFrame, name: str) -> db.BlenderObject:
    vertices = np.zeros((len(df), 3), dtype=np.float32)
    bob = db.create_bob(vertices, name=name)

    update_bob_from_polars_df(bob, df)
    return bob


def update_bob_from_polars_df(bob: db.BlenderObject, df: pl.DataFrame) -> None:
    for col in df.columns:
        col_dtype = df[col].dtype
        if col_dtype in [pl.Utf8]:
            continue
        data = df[col].to_numpy()
        bob.store_named_attribute(data, col)


def update_obj_from_csv(obj: bpy.types.Object, csv_file: str) -> None:
    bob = db.BlenderObject(obj)
    df = pl.read_csv(csv_file)
    if len(df) != len(bob):
        bob.new_from_pydata(np.zeros((len(df), 3), dtype=np.float32))
    update_bob_from_polars_df(bob, df)
