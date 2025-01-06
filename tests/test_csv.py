import pytest
from pathlib import Path
import bpy
from databpy.object import ObjectTracker, BlenderObject
import polars as pl
import numpy as np

DATA_FOLDER = Path(__file__).parent / "data"


def test_import_via_operator(snapshot):
    deno_path = str(DATA_FOLDER / "deno_star_elemens.csv")

    with ObjectTracker() as o:
        bpy.ops.import_scene.import_csv_polars(filepath=deno_path)
        bob = BlenderObject(o.latest())

    # created mesh is the size we expect
    assert len(bob) == 142

    # the data from the mesh is the same as that from the dataframe
    df = pl.read_csv(deno_path)
    assert np.allclose(bob.named_attribute("Dino_X"), df["Dino_X"].to_numpy())
