import databpy as db
import polars as pl
import numpy as np
import bpy


def polars_df_to_bob(df: pl.DataFrame, name: str) -> db.BlenderObject:
    vertices = np.zeros((len(df), 3), dtype=np.float32)
    bob = db.create_bob(vertices, name=name)

    update_bob_from_polars_df(bob, df)
    return bob


def update_obj_from_csv(obj: bpy.types.Object, csv_file: str) -> None:
    bob = db.BlenderObject(obj)
    df = pl.read_csv(csv_file)
    if len(df) != len(bob):
        bob.new_from_pydata(np.zeros((len(df), 3), dtype=np.float32))
    update_bob_from_polars_df(bob, df)


def update_bob_from_polars_df(bob: db.BlenderObject, df: pl.DataFrame) -> None:
    for col in df.columns:
        col_dtype = df[col].dtype
        if col_dtype in [pl.Utf8]:  # skip strings
            continue
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
