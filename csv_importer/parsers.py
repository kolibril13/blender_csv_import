import databpy as db
import polars as pl
import numpy as np
import bpy
import warnings


def polars_df_to_bob(df: pl.DataFrame, name: str, string_limit: int = 3000) -> db.BlenderObject:
    vertices = np.zeros((len(df), 3), dtype=np.float32)
    bob = db.create_bob(vertices, name=name)

    update_bob_from_polars_df(bob, df, string_limit=string_limit)
    return bob

 
def update_obj_from_csv(obj: bpy.types.Object, csv_file: str, string_limit: int = 3000) -> None:
    bob = db.BlenderObject(obj)
    df = pl.read_csv(csv_file)
    if len(df) != len(bob):
        bob.new_from_pydata(np.zeros((len(df), 3), dtype=np.float32))
    update_bob_from_polars_df(bob, df, string_limit=string_limit)


def update_bob_from_polars_df(bob: db.BlenderObject, df: pl.DataFrame, string_limit: int = 3000) -> None:
    for col in df.columns:
        col_dtype = df[col].dtype
        if col_dtype in [pl.Utf8]:  # handle strings
            # Convert to numpy array and fill nulls with empty string
            data = df[col].fill_null("").to_numpy()
            unique, encoding = np.unique(data, return_inverse=True)
            # Only add strings when there are less than the string limit
            if len(unique) <= string_limit:
                bob.store_named_attribute(encoding, col)
                db.nodes.custom_string_iswitch("{}: {}".format(bob.name, col), unique, col)
            else:
                warnings.warn(f"Column '{col}' has {len(unique)} unique strings, which exceeds the limit of {string_limit}. "
                              f"This column will be skipped. You can increase the limit with the string_limit parameter.")
        else:
            data = np.vstack(df[col].to_numpy())
            bob.store_named_attribute(data, col)

    """
    Converts a Polars DataFrame into a Blender object (bob) and stores its columns as named attributes.

    `np.vstack` is used to ensure that 3D vectors are properly porcessed.
    
    Example:

        import polars as pl
        import numpy as np
        import databpy as db

        # Create a DataFrame
        df = pl.DataFrame({
            "Star": [
                [58.2136, 91.8819, 0.0],
                [58.1961, 92.215, 0.0]
            ],
            "Is_Visible": [True, False],
            "Intensity": [10, 20],
        })

        #  convert "Star" column to a NumPy array (won't work in databpy)
        df["Star"].to_numpy()
        # Output:
        # array([array([58.2136, 91.8819,  0.    ]),
        #        array([58.1961, 92.215 ,  0.    ])], dtype=object)

        # Use np.vstack to stack the arrays vertically (this will work in databpy)
        np.vstack(df["Star"].to_numpy())
        # Output:
        # array([[58.2136, 91.8819,  0.    ],
        #        [58.1961, 92.215 ,  0.    ]])

        vertices = np.zeros((len(df), 3), dtype=np.float32)
        bob = db.create_bob(vertices, name="DataWithVector")

        for col in df.columns:
            data = np.vstack(df[col].to_numpy())
            bob.store_named_attribute(data, col)

    """
