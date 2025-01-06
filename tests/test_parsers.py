import unittest
import polars as pl
import numpy as np
from csv_importer.parsers import polars_df_to_bob


class TestParsers(unittest.TestCase):
    def setUp(self):
        # Create sample test data
        self.test_df = pl.DataFrame(
            {
                "x": [1.0, 2.0, 3.0],
                "y": [4.0, 5.0, 6.0],
                "z": [7.0, 8.0, 9.0],
                "label": ["a", "b", "c"],
            }
        )

    def test_polars_df_to_bob(self):
        bob = polars_df_to_bob(self.test_df, name="test_object")
        self.assertEqual(bob.name, "test_object")
        self.assertEqual(len(bob.vertices), 3)
