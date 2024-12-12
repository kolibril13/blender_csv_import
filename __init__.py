import bpy
import polars as pl
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from .polars_mesh import PolarsMesh
import time

# Operator for the button
class ImportCsvPolarsOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "import_scene.import_csv_polars"
    bl_label = "Import CSV (Polars)"
    bl_options = {'PRESET', 'UNDO'}

    # ImportHelper mix-in class uses this
    filename_ext = ".csv"
    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        CSV_FILE = self.filepath  # Use the selected file path

        # Read CSV with Polars
        df_polars = pl.read_csv(CSV_FILE)

        # Measure execution time
        start_time = time.perf_counter()
        
        # Create a PolarsMesh object
        blender_mesh = PolarsMesh(dataframe=df_polars, object_name="ImportedMesh")

        # Link the new mesh to the Blender scene
        bpy.context.collection.objects.link(blender_mesh.point_obj)

        # Calculate elapsed time in milliseconds
        elapsed_time_ms = (time.perf_counter() - start_time) * 1000

        # Report result with execution time
        self.report({'INFO'}, f" 🐻‍❄️ 📥  Added {blender_mesh.object_name} in {elapsed_time_ms:.2f} ms")
        return {'FINISHED'}

# Register the operator and menu entry
def menu_func_import(self, context):
    self.layout.operator(ImportCsvPolarsOperator.bl_idname, text="CSV 🐻 (.csv)")

# Register the operator and the menu
def register():
    bpy.utils.register_class(ImportCsvPolarsOperator)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

# Unregister the operator and the menu
def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.utils.unregister_class(ImportCsvPolarsOperator)

# Initialize
if __name__ == "__main__":
    register()