import databpy as db
import polars as pl
import bpy


def from_blender_to_polars_df(blender_object: bpy.types.Object) -> pl.DataFrame:
    """
    Convert a Blender mesh object to a basic Polars DataFrame containing mesh attributes.
    
    Args:
        blender_object: The Blender object to convert
        
    Returns:
        pl.DataFrame: Basic DataFrame containing raw mesh attribute data
    """
    # Evaluate the object and get mesh data
    evaluated_obj = db.evaluate_object(blender_object)
    mesh = evaluated_obj.to_mesh()

    # Collect all attribute data
    attribute_data = {}
    for attr in mesh.attributes:
        if attr.name not in {'sharp_face', 'UVMap'} and not attr.name.startswith('.'):
            a = db.named_attribute(evaluated_obj, attr.name)
            attribute_data[attr.name] = a

    # Create and return basic polars DataFrame
    return pl.DataFrame(attribute_data)


def from_polars_df_to_csv(df: pl.DataFrame, export_path: str) -> None:
    """
    Process a Polars DataFrame and export it to a CSV file.
    Handles array expansion, column reordering, and CSV writing.
    
    Args:
        df: The Polars DataFrame to process and export
        export_path: The file path where the CSV should be saved
    """
    # Sort columns so "position" is first
    if "position" in df.columns:
        column_order = ["position"] + [col for col in df.columns if col != "position"]
        df = df.select(column_order)

    # Check dtypes and expand array columns
    dtypes = df.dtypes
    array_columns = []
    expanded_df = df.clone()

    for i, dtype in enumerate(dtypes):
        col_name = df.columns[i]
        if str(dtype).startswith('Array'):
            array_columns.append(col_name)
            
            # Get the array length from the first non-null value
            first_array = expanded_df.select(pl.col(col_name)).item(0, 0)
            array_length = len(first_array)
            
            # Expand array into separate columns with indexed names
            for j in range(array_length):
                expanded_df = expanded_df.with_columns([
                    pl.col(col_name).arr.get(j).alias(f"{col_name}{j+1}")
                ])
            # Drop the original array column
            expanded_df = expanded_df.drop(col_name)

    # Reorder columns to place position columns first
    position_columns = [col for col in expanded_df.columns if col.startswith('position')]
    other_columns = [col for col in expanded_df.columns if not col.startswith('position')]
    column_order = position_columns + other_columns
    expanded_df = expanded_df.select(column_order)

    # Write processed DataFrame to CSV file
    expanded_df.write_csv(export_path) 