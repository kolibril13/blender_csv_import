import pytest
from pathlib import Path
import bpy
from databpy.object import ObjectTracker, BlenderObject
import polars as pl
import numpy as np
from csv_importer.csv import load_csv
import tempfile


DATA_FOLDER = Path(__file__).parent / "data"


def test_import_via_operator():
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


def test_csv_with_strings():
    csv_path = DATA_FOLDER / "example_string.csv"
    obj = load_csv(str(csv_path))
    bob = BlenderObject(obj)
    assert bob.name == "CSV_example_string"
    assert len(bob) == 10
    assert len(bob.named_attribute("City1")) == 10
    node = bpy.data.node_groups.get("CSV_example_string: City1")
    assert node is not None
    assert node.interface.items_tree["City1"].in_out == "INPUT"
    assert node.interface.items_tree["String"].in_out == "OUTPUT"
    assert len(node.nodes["Index Switch"].inputs) == 12


def test_csv_with_strings_missing():
    csv_path = DATA_FOLDER / "missing_string.csv"
    obj = load_csv(str(csv_path))
    bob = BlenderObject(obj)
    assert len(bob) == 3
