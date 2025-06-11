from bpy.types import PropertyGroup
from bpy.props import StringProperty, IntProperty, BoolProperty


class CSVImporterObjectProperties(PropertyGroup):
    filepath: StringProperty(  # type: ignore
        name="CSV Filepath",
        description="Path to the CSV file that was used for loading this object",
        subtype="FILE_PATH",
        default="",
    )

    last_loaded_time: IntProperty(  # type: ignore
        name="File Access Time",
        description="The last time the file was accessed",
        default=0,
    )

    hot_reload: BoolProperty(  # type: ignore
        name="Hot Reload",
        description="Whether to reload the CSV file when the object is selected",
        default=False,
    )


class CSVExporterSceneProperties(PropertyGroup):
    export_path: StringProperty(  # type: ignore
        name="Export Path",
        description="Path where the CSV file will be exported",
        subtype="FILE_PATH",
        default="//exported_data.csv",
    )


CLASSES = (CSVImporterObjectProperties, CSVExporterSceneProperties)
