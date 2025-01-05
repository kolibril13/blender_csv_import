import polars as pl
import numpy as np
import databpy as db
import bpy

from bpy.props import StringProperty

import time

from .csv import load_csv


# based on the blender docs: https://docs.blender.org/api/current/bpy.types.FileHandler.html#basic-filehandler-for-operator-that-imports-just-one-file
# and tweaked with this prompt: https://chatgpt.com/share/675b0831-354c-8013-bae0-9bb91d527f32


# Operator for the button and drag-and-drop
class ImportCsvPolarsOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "import_scene.import_csv_polars"
    bl_label = "Import CSV (Polars)"
    bl_options = {"PRESET", "UNDO"}

    # ImportHelper mix-in provides 'filepath' by default, but we redefine it here
    # to use SKIP_SAVE, allowing drag-and-drop to work properly.
    filepath: StringProperty(subtype="FILE_PATH", options={"SKIP_SAVE"})  # type: ignore

    filename_ext = ".csv"
    filter_glob: StringProperty(  # type: ignore
        default="*.csv",
        options={"HIDDEN"},
        maxlen=255,
    )

    def execute(self, context):
        # Ensure the filepath is a CSV file

        if not self.filepath.lower().endswith(".csv"):
            self.report({"WARNING"}, "Selected file is not a CSV")
            return {"CANCELLED"}

        start_time = time.perf_counter()

        load_csv(filepath=self.filepath)

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
