import pytest
from pathlib import Path
import bpy
from databpy.object import ObjectTracker, BlenderObject
import polars as pl
import numpy as np
from csv_importer.csv import load_csv
import tempfile


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


@pytest.fixture
def setup_csv():
    # Create a temporary CSV file for testing
    temp_dir = tempfile.mkdtemp()
    test_csv = Path(temp_dir) / "test.csv"
    with open(test_csv, "w") as f:
        f.write("x,y,z\n1,2,3\n4,5,6\n7,8,9")
    yield test_csv
    # Clean up temporary files
    test_csv.unlink()
    Path(temp_dir).rmdir()


def test_load_csv(setup_csv):
    obj = load_csv(str(setup_csv))
    assert obj.name == "CSV_test"
    assert len(obj.data.vertices) == 3
