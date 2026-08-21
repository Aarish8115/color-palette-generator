import pandas as pd

def load_colors(path: str = "data/cleaned-colors.parquet") -> pd.DataFrame:
    """
    Loads the color dataset and adds derived in-memory columns needed 
    by the rest of the pipeline. Does NOT modify or resave the source 
    parquet file — this is purely a runtime adaptation layer.
    """
    df = pd.read_parquet(path)

    # color_id: use the dataframe's row index directly, in-memory only
    df["color_id"] = df.index

    # split hsl list column into separate numeric columns
    df["Hue"] = df["hsl"].apply(lambda x: x[0])
    df["Saturation"] = df["hsl"].apply(lambda x: x[1])
    df["Lightness"] = df["hsl"].apply(lambda x: x[2])

    # split rgb list column into separate numeric columns (if needed anywhere)
    df["R"] = df["rgb"].apply(lambda x: x[0])
    df["G"] = df["rgb"].apply(lambda x: x[1])
    df["B"] = df["rgb"].apply(lambda x: x[2])

    return df
