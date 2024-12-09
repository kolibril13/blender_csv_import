import bpy
import polars as pl
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
from .polars_mesh import PolarsMesh
import time

# Operator for the button
class ImportCsvPolarsOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "wm.import_csv_polars_operator"
    bl_label = "Import CSV (Polars)"

    # ImportHelper mix-in class uses this
    filename_ext = ".csv"
    filter_glob: StringProperty(
        default="*.csv",
        options={'HIDDEN'},
        maxlen=255,
    )

    def execute(self, context):
        CSV_FILE = self.filepath  # Use the selected file path
        # CSV_FILE = "de.csv"

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
        self.report({'INFO'}, f" 🐻‍❄️ 📥 Grrr!! Added {blender_mesh.object_name} in {elapsed_time_ms:.2f} ms")
        return {'FINISHED'}

# Function to add the button to the World Scene Panel
class WORLD_PT_import_csv_panel(bpy.types.Panel):
    bl_label = "Import CSV with Polars"
    bl_idname = "WORLD_PT_import_csv_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "world"  # This targets the World Properties tab

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.import_csv_polars_operator", text="🐻‍❄️📥 Polars Import", emboss=True)

# Register the operator and the panel
def register():
    bpy.utils.register_class(ImportCsvPolarsOperator)
    bpy.utils.register_class(WORLD_PT_import_csv_panel)

# Unregister the operator and the panel
def unregister():
    bpy.utils.unregister_class(WORLD_PT_import_csv_panel)
    bpy.utils.unregister_class(ImportCsvPolarsOperator)

# Initialize
if __name__ == "__main__":
    register()