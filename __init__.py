import bpy
import polars as pl
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty

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
        # CSV_FILE = "random_coordinates.csv"

        df_polars = pl.read_csv(CSV_FILE)

        mesh = bpy.data.meshes.new("PointCloudMesh")
        icebear_obj = bpy.data.objects.new("IceBear", mesh)
        bpy.context.collection.objects.link(icebear_obj)
        
        length = len(df_polars)
        vertices = [(0, 0, 0) for _ in range(length)]
        mesh.from_pydata(vertices, [], [])
        mesh.update()
        
        # Add each attribute individually to the mesh 
        lat_attr = mesh.attributes.new(name='coord1', type='FLOAT', domain='POINT')
        lng_attr = mesh.attributes.new(name='coord2', type='FLOAT', domain='POINT') 
        
        # Set the values for the attributes
        lat_attr.data.foreach_set('value', df_polars['x'])
        lng_attr.data.foreach_set('value', df_polars['y'])
        
        mesh.update()
        
        self.report({'INFO'}, f" 🐻‍❄️ 📥 Grrr!! Added {icebear_obj}")
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