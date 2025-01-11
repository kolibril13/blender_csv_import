import bpy


class CSV_PT_ObjectPanel(bpy.types.Panel):
    bl_label = "CSV Importer"
    bl_idname = "CSV_PT_ObjectPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_order = 0
    bl_options = {"HEADER_LAYOUT_EXPAND"}
    # bl_ui_units_x = 0

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        scene = context.scene

        row = layout.row(align=False)
        row.prop(obj.csv, "csv_filepath", text="")
        row.enabled = False
        op = layout.operator("csv.reload_data")
        op.filepath = obj.csv.csv_filepath


CLASSES = (CSV_PT_ObjectPanel,)
