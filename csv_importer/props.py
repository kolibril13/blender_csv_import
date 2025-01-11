from bpy.types import PropertyGroup
from bpy.props import StringProperty


class CSVImporterObjectProperties(PropertyGroup):
    csv_filepath: StringProperty(  # type: ignore
        name="CSV Filepath",
        description="Path to the CSV file that was used for loading this object",
        subtype="FILE_PATH",
        default="",
    )


CLASSES = (CSVImporterObjectProperties,)
