import bpy
from . import ops, props, ui
from .props import CSVImporterObjectProperties
from bpy.props import PointerProperty
from .ui import CSV_PT_ObjectPanel

CLASSES = ops.CLASSES + props.CLASSES + ui.CLASSES


# Register the operator and menu entry
def menu_func_import(self, context):
    self.layout.operator(ImportCsvPolarsOperator.bl_idname, text="CSV 🐻 (.csv)")


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.Object.csv = PointerProperty(type=CSVImporterObjectProperties)  # type: ignore


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.csv  # type: ignore
