import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty

import polars as pl
import numpy as np
import databpy as db

from io import StringIO
from pathlib import Path
import time

# based on the blender docs: https://docs.blender.org/api/current/bpy.types.FileHandler.html#basic-filehandler-for-operator-that-imports-just-one-file
# and tweaked with this prompt: https://chatgpt.com/share/675b0831-354c-8013-bae0-9bb91d527f32


# Operator for the button and drag-and-drop
class ImportCsvPolarsOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "import_scene.import_csv_polars"
    bl_label = "Import CSV (Polars)"
    bl_options = {"PRESET", "UNDO"}

    # ImportHelper mix-in provides 'filepath' by default, but we redefine it here
    # to use SKIP_SAVE, allowing drag-and-drop to work properly.
    filepath: StringProperty(subtype="FILE_PATH", options={"SKIP_SAVE"})

    filename_ext = ".csv"
    filter_glob: StringProperty(
        default="*.csv",
        options={"HIDDEN"},
        maxlen=255,
    )

    def execute(self, context):
        # Ensure the filepath is a CSV file

        if not self.filepath.lower().endswith(".csv"):
            self.report({"WARNING"}, "Selected file is not a CSV")
            return {"CANCELLED"}

        # Use the selected/dropped file path
        csv_file = Path(self.filepath)
        file_name_without_ext = csv_file.stem
        start_time = time.perf_counter()

        df = pl.read_csv(csv_file)

        vertices = np.zeros((len(df), 3), dtype=np.float32)
        bob = db.create_bob(vertices, name=f"CSV_{file_name_without_ext}")

        for col in df.columns:
            col_dtype = df[col].dtype
            if col_dtype in [pl.Utf8]:
                continue
            data = df[col].to_numpy()
            bob.store_named_attribute(data, col)

        elapsed_time_ms = (time.perf_counter() - start_time) * 1000

        self.report(
            {"INFO"},
            f" 🐻‍❄️ 📥  Added {bob.name} in {elapsed_time_ms:.2f} ms",
        )
        return {"FINISHED"}

    def invoke(self, context, event):
        # If the filepath is already set (e.g. drag-and-drop), execute directly
        if self.filepath:
            return self.execute(context)
        # Otherwise, show the file browser
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


# File Handler for drag-and-drop support
class CSV_FH_import(bpy.types.FileHandler):
    bl_idname = "CSV_FH_import"
    bl_label = "File handler for CSV import"
    bl_import_operator = "import_scene.import_csv_polars"
    bl_file_extensions = ".csv"

    @classmethod
    def poll_drop(cls, context):
        # Allow drag-and-drop in the 3D View
        return context.area and context.area.type == "VIEW_3D"


# Register the operator and menu entry
def menu_func_import(self, context):
    self.layout.operator(ImportCsvPolarsOperator.bl_idname, text="CSV 🐻 (.csv)")


def register():
    bpy.utils.register_class(ImportCsvPolarsOperator)
    bpy.utils.register_class(CSV_FH_import)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.utils.unregister_class(CSV_FH_import)
    bpy.utils.unregister_class(ImportCsvPolarsOperator)


if __name__ == "__main__":
    register()
