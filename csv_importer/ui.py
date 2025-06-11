import bpy


class CSV_PT_ObjectPanel(bpy.types.Panel):
    bl_label = "CSV Importer"
    bl_idname = "CSV_PT_ObjectPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_order = 0
    bl_options = {"HEADER_LAYOUT_EXPAND"}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == "MESH" and obj.csv.filepath != ""

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        scene = context.scene

        row = layout.row(align=False)
        row.prop(obj.csv, "filepath", text="")
        row.enabled = False
        row = layout.row(align=True)
        col = row.column()
        op = col.operator("csv.reload_data")
        col.enabled = not obj.csv.hot_reload
        op.filepath = obj.csv.filepath

        # if obj.csv.hot_reload and op._timer is not None:
        if obj.csv.hot_reload:
            message = "Hot Reload"
            icon = "PAUSE"
        else:
            message = "Hot Reload"
            icon = "PLAY"
        op = row.operator(
            "csv.toggle_hot_reload", text=message, icon=icon, depress=obj.csv.hot_reload
        )


class CSV_PT_ExportPanel(bpy.types.Panel):
    bl_label = "Export"
    bl_idname = "CSV_PT_ExportPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_order = 0
    bl_options = {"HEADER_LAYOUT_EXPAND"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Export path field
        row = layout.row()
        row.prop(scene.csv_export, "export_path", text="Export Path")
        
        # Export button
        row = layout.row()
        row.operator("csv.export_data", text="Export CSV", icon="EXPORT")


CLASSES = (CSV_PT_ObjectPanel, CSV_PT_ExportPanel)
