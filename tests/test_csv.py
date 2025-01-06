import pytest
from pathlib import Path
import bpy

DATA_FOLDER = Path(__file__).parent / "data"


def test_import_via_operator():
    bpy.ops.import_scene.import_csv_polars(
        filepath=str(DATA_FOLDER / "deno_star_elemens.csv")
    )
