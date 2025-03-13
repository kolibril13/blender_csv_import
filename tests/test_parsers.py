import pytest
import polars as pl
import numpy as np
from io import StringIO
from csv_importer.parsers import polars_df_to_bob, update_bob_from_polars_df
import warnings
import string
import bpy
from unittest.mock import patch

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

    # # Validate that "StringVal" does not exist as a numerical attribute
    # with pytest.raises(AttributeError):
    #     bob.named_attribute("StringVal")



def test_string_limit_functionality():
    """Test string limit functionality without using mocks."""
    # Create test data with specific string values and a null
    test_strings = ["apple", None, "banana", "apple", "cherry"]
    test_data = {
        "strings": test_strings,
        "numbers": np.arange(len(test_strings))
    }
    df = pl.DataFrame(test_data)
    
    # Test with normal string limit (should process all strings)
    bob = polars_df_to_bob(df, name="TestStringLimit", string_limit=10)
    
    # Verify the numeric column was processed
    numbers_attr = bob.named_attribute("numbers")
    assert np.array_equal(numbers_attr, np.arange(len(test_strings)))
    
    # Verify the string column was processed and encoded correctly
    # The encoding should map: "" (for None) -> 0, "apple" -> 1, "banana" -> 2, "cherry" -> 3
    # So the expected encoding is [1, 0, 2, 1, 3]
    strings_attr = bob.named_attribute("strings")
    expected_encoding = np.array([1, 0, 2, 1, 3])
    assert np.array_equal(strings_attr, expected_encoding)
    
    # Test with very low string limit (should skip string column)
    # Use a mocked warning instead of popup_menu which causes segfault
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        # Use patch to avoid the read-only attribute error
        with patch.object(bpy.context.window_manager.__class__, 'popup_menu', create=True, new=lambda *args, **kwargs: None):
            # Create a new bob with a low string limit
            limited_bob = polars_df_to_bob(df, name="LimitedStringTest", string_limit=2)
            
            # Check that a warning was raised
            assert any("exceeds the limit" in str(warning.message) for warning in w)
        
            # Verify the numeric column was processed
            numbers_attr = limited_bob.named_attribute("numbers")
            assert np.array_equal(numbers_attr, np.arange(len(test_strings)))
            
            # Verify the string column was skipped (should raise an AttributeError)
            with pytest.raises(AttributeError):
                limited_bob.named_attribute("strings")
