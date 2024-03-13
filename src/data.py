import pandas as pd


def get_data(dataPath: str, wave: int, cols: list):
    """
    Load the data from the specified wave and columns.
    Args:
        - dataPath: the path to the data.
        - wave: the wave of the data.
        - cols: the columns to load.
    Returns:
        - df: the dataset.
    """

    df = pd.DataFrame()
    cols_tag = [col[:2] for col in cols]
    for tag in cols_tag:
        path = f'{dataPath}/sharew{wave}_rel8-0-0_ALL_datasets_stata/sharew{wave}_rel8-0-0_{tag}.dta'
        data = pd.read_stata(path)
        df = pd.concat([df, data], axis=1)
    df = df[cols]
    df = df.loc[:,~df.columns.duplicated()]
    return df