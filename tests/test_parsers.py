import pytest
import polars as pl
from csv_importer.parsers import polars_df_to_bob


@pytest.fixture
def test_df():
    return pl.DataFrame(
        {
            "x": [1.0, 2.0, 3.0],
            "y": [4.0, 5.0, 6.0],
            "z": [7.0, 8.0, 9.0],
            "label": ["a", "b", "c"],
        }
    )


def test_polars_df_to_bob(test_df):
    # Test if polars_df_to_bob converts a Polars DataFrame to a Bob object

    bob = polars_df_to_bob(test_df, name="test_object")
    assert bob.name == "test_object"
    assert len(bob.vertices) == 3


import numpy as np
import bpy
from io import StringIO


def test_polars_df_to_bob_with_datatypes():
    # Simulate CSV data with multiple data types: float, integer, boolean, and string


    # Info: Don't add spaces for indentation in front of the below string. It would cause this test to fail.
    csv_data = StringIO(
        """
FloatVal,IntVal,BoolVal,StringVal
1.23,10,true,Hello
4.56,20,false,World"""
    )

    # Create a Polars DataFrame
    df = pl.read_csv(csv_data)

    # Convert DataFrame to Bob object
    bob = polars_df_to_bob(df, name="TestObject")
    obj = bpy.data.objects["TestObject"]

    print("Available attributes:", obj.data.attributes.keys())
    # Validate that the Bob object has the correct attributes
    float_val_attr = bob.named_attribute("FloatVal")
    int_val_attr = bob.named_attribute("IntVal")
    bool_val_attr = bob.named_attribute("BoolVal")

    # Compare attributes with original DataFrame data
    assert np.allclose(float_val_attr, df["FloatVal"].to_numpy()), "FloatVal mismatch"
    assert np.array_equal(int_val_attr, df["IntVal"].to_numpy()), "IntVal mismatch"
    assert np.array_equal(
        bool_val_attr.astype(bool), df["BoolVal"].to_numpy()
    ), "BoolVal mismatch"

    # Validate that "StringVal" does not exist as a numerical attribute
    with pytest.raises(AttributeError):
        bob.named_attribute("StringVal")
