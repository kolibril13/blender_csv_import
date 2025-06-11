import bpy
from . import ops, props, ui
from .props import CSVImporterObjectProperties, CSVExporterSceneProperties
from bpy.props import PointerProperty, EnumProperty
from .ops import ImportCsvPolarsOperator
from .utils import add_current_module_to_path

CLASSES = ops.CLASSES + props.CLASSES + ui.CLASSES


# Register the operator and menu entry
def menu_func_import(self, context):
    self.layout.operator(ImportCsvPolarsOperator.bl_idname, text="CSV 🐻 (.csv)")


def register():
    add_current_module_to_path()
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.Object.csv = PointerProperty(type=CSVImporterObjectProperties)  # type: ignore
    bpy.types.Scene.csv_export = PointerProperty(type=CSVExporterSceneProperties)  # type: ignore
    
    # Add export type property to window manager for UI
    bpy.types.WindowManager.csv_export_type = EnumProperty(  # type: ignore
        name="Export Type",
        description="Type of file to export",
        items=[
            ('CSV', "CSV", "Export as CSV"),
            ('JSON', "JSON", "Export as JSON"), 
            ('PARQUET', "Parquet", "Export as Parquet")
        ],
        default='CSV'
    )


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.csv  # type: ignore
    del bpy.types.Scene.csv_export  # type: ignore
    del bpy.types.WindowManager.csv_export_type  # type: ignore
