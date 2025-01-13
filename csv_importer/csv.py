from pathlib import Path
import polars as pl
from bpy.types import Object
from .parsers import polars_df_to_bob
from . import addon


def load_csv(filepath: str) -> Object:
    # Use the selected/dropped file path
    csv_file = Path(filepath)
    file_name_without_ext = csv_file.stem

    df = pl.read_csv(csv_file)
    bob = polars_df_to_bob(df, name=f"CSV_{file_name_without_ext}")
    try:
        bob.object.csv.filepath = str(csv_file)
    except AttributeError:
        addon.register()
        bob.object.csv.filepath = str(csv_file)

    return bob.object
