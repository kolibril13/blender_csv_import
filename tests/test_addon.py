import unittest
import bpy
from csv_importer.addon import register, unregister


class TestAddon(unittest.TestCase):
    def test_register_unregister(self):
        self.assertIn("import_csv_polars", bpy.ops.import_scene.__dir__())

        # Test unregistration
        unregister()
        self.assertNotIn("import_csv_polars", bpy.ops.import_scene.__dir__())
        register()
