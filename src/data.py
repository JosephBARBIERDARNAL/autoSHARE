import pandas as pd
import streamlit as st

from src.utils import clean_suffix_from_cols, load_data_properties


class DatasetManager:
    """
    Class to handle the dataset.
    """

    def __init__(self, data_path: str, wave: int):
        self.data_path = data_path
        self.wave = wave

    def create_dataframe(self, cols: list):
        """
        Load the data from the specified columns.
        Args:
            - cols: the columns to load.
        Returns:
            - df: the dataset.
        """

        columns_properties = load_data_properties(self.wave)
        df = pd.DataFrame()

        # get all files needed
        file_names = []
        for col in cols:
            file_name = columns_properties.loc[
                columns_properties["column"] == col, "file_name"
            ].values[0]
            if file_name not in file_names:
                file_names.append(file_name)
        file_names.append(f"wave{self.wave}_dummy.stata")

        # load all datasets
        for file_name in file_names:
            full_path = f"{self.data_path}/sharew{self.wave}_rel9-0-0_ALL_datasets_stata/{file_name}"
            temp = pd.read_stata(full_path, convert_categoricals=False)

            # merge with mergeid
            if len(df) == 0:
                df = temp
            else:
                if "mergeid" not in temp.columns:
                    st.write(
                        f"mergeid not found in {file_name} (removed from the dataset)"
                    )
                else:
                    df = df.merge(temp, on="mergeid", how="outer")

        # add country and language
        cols.extend(["country", "language"])

        # remove dupplicate columns from merging
        df = clean_suffix_from_cols(df)

        # keep only the selected columns
        cols = list(set(cols))
        df = df[cols]

        # output
        self.df = df
        return df
