import pytest
import bpy
from csv_importer.addon import register, unregister


def test_register_unregister():
    assert "import_csv_polars" in dir(bpy.ops.import_scene)

    # Test unregistration
    unregister()
    assert "import_csv_polars" not in dir(bpy.ops.import_scene)
    register()
