import streamlit as st
import pandas as pd



@st.cache_data(show_spinner=False)
def clean_suffix_from_cols(df):
    """
    For each column, check if
    there is another columns that is the same
    with a suffix like _x or _y. If so, remove
    the suffix and keep only the first column.
    """

    # check for suffixes
    for col in df.columns:

        # if has a suffix
        if col[-2:] == '_x' or col[-2:] == '_y':

            # remove old column and add new one
            df[col[:-2]] = df[col]
            df.drop(col, axis=1, inplace=True)

    return df


@st.cache_data(show_spinner=False)
def load_data_properties(wave: int, data_path: str = 'static/columns'):
    """
    Load the properties/meta-data of the columns for the specified wave.
    """
    columns_properties = pd.read_csv(f'{data_path}/wave_{wave}_columns.csv')
    return columns_properties