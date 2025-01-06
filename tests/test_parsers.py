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
    bob = polars_df_to_bob(test_df, name="test_object")
    assert bob.name == "test_object"
    assert len(bob.vertices) == 3
