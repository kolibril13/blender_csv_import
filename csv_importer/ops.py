import bpy
from bpy.props import StringProperty
import time
from bpy_extras.io_utils import ImportHelper, ExportHelper
from .csv import load_csv
from .parsers import update_obj_from_csv
from pathlib import Path
from .exporters import from_blender_to_polars_df, from_polars_df_to_csv

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

        bob = load_csv(filepath=self.filepath)
        bob.csv.filepath = self.filepath

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
        # Allow drag-and-drop
        return context.area


class ExportCsvPolarsOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "export_scene.export_csv_polars"
    bl_label = "Export CSV (Polars)"
    bl_options = {"PRESET", "UNDO"}

    filepath: StringProperty(subtype="FILE_PATH")  # type: ignore

    filename_ext = ".csv"
    filter_glob: StringProperty(  # type: ignore
        default="*.csv",
        options={"HIDDEN"},
        maxlen=255,
    )

    def execute(self, context):
        export_object = context.active_object
        
        if export_object is None:
            self.report({"WARNING"}, "No object selected")
            return {"CANCELLED"}
            
        if export_object.type != "MESH":
            self.report({"WARNING"}, "Selected object is not a mesh")
            return {"CANCELLED"}

        start_time = time.perf_counter()

        df = from_blender_to_polars_df(export_object)
        from_polars_df_to_csv(df, self.filepath)

        elapsed_time_ms = (time.perf_counter() - start_time) * 1000

        self.report(
            {"INFO"},
            f" 🐻‍❄️ 📤  Exported {export_object.name} in {elapsed_time_ms:.2f} ms",
        )
        return {"FINISHED"}


class CSV_OP_ReloadData(bpy.types.Operator):
    bl_idname = "csv.reload_data"
    bl_label = "Reload Data"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = (
        "Reload the imported data file with updated values into this object"
    )

    filepath: StringProperty(  # type: ignore
        subtype="FILE_PATH", name="File Path", description="Path to the CSV file"
    )

    def execute(self, context):
        obj: bpy.types.Object = bpy.context.active_object  # type: ignore
        n_points = len(obj.data.vertices)
        update_obj_from_csv(obj, self.filepath)
        message = f"Reloaded data for {len(obj.data.vertices)} points"
        if len(obj.data.vertices) != n_points:
            message += f" (was {n_points})"
        self.report({"INFO"}, message=message)
        return {"FINISHED"}


def hot_reload_timer():
    # The actual hot reload logic
    for obj in bpy.data.objects:
        path = Path(obj.csv.filepath)
        if not obj.csv.hot_reload:
            continue
        if not path.exists():
            obj.csv.hot_reload = False
            continue
        if obj.csv.last_loaded_time < path.stat().st_mtime:
            update_obj_from_csv(obj, str(path))
            obj.csv.last_loaded_time = int(time.time())

    return 1.0  # Run again in 1 second


class CSV_OT_ToggleHotReload(bpy.types.Operator):
    bl_idname = "csv.toggle_hot_reload"
    bl_label = "Toggle Hot Reload"
    bl_description = (
        "Enable or disable hot reloading of the data from the imported file"
    )

    def execute(self, context):
        obj = context.active_object
        if obj.csv.hot_reload:
            try:
                bpy.app.timers.unregister(hot_reload_timer)
            except Exception as e:
                print(e)
            obj.csv.hot_reload = False
            self.report({"INFO"}, "Hot reload stopped")
        else:
            bpy.app.timers.register(hot_reload_timer)
            obj.csv.hot_reload = True
            self.report({"INFO"}, "Hot reload started")
        return {"FINISHED"}


CLASSES = (
    ImportCsvPolarsOperator,
    CSV_FH_import,
    ExportCsvPolarsOperator,
    CSV_OP_ReloadData,
    CSV_OT_ToggleHotReload,
)
