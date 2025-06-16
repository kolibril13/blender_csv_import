import bpy
from . import ops, props, ui
from .props import CSVImporterObjectProperties
from bpy.props import PointerProperty
from .ops import ImportCsvPolarsOperator, ExportCsvPolarsOperator, ExportJsonPolarsOperator
from .utils import add_current_module_to_path

CLASSES = ops.CLASSES + props.CLASSES + ui.CLASSES


# Register the operator and menu entry
def menu_func_import(self, context):
    self.layout.operator(ImportCsvPolarsOperator.bl_idname, text="CSV 🐻 (.csv)")

def menu_func_export(self, context):
    self.layout.operator(ExportCsvPolarsOperator.bl_idname, text="CSV 🐻 (.csv)")
    self.layout.operator(ExportJsonPolarsOperator.bl_idname, text="JSON 🐻 (.json)")


def register():
    add_current_module_to_path()
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.Object.csv = PointerProperty(type=CSVImporterObjectProperties)  # type: ignore


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.csv  # type: ignore
