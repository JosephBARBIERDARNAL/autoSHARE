import pandas as pd
import streamlit as st
from src.ui import make_space



@st.cache_data(show_spinner=False)
def load_data_properties(wave: int):
    """
    Load the properties of the columns for the specified wave.
    """
    columns_properties = pd.read_csv(f'static/columns/wave_{wave}_columns.csv')
    return columns_properties




class datasetManager:

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
            file_name = columns_properties.loc[columns_properties['column']==col, 'file_name'].values[0]
            if file_name not in file_names:
                file_names.append(file_name)

        # load all datasets
        for file_name in file_names:
            full_path = f'{self.data_path}/sharew{self.wave}_rel9-0-0_ALL_datasets_stata/{file_name}'
            temp = pd.read_stata(
                full_path,
                convert_categoricals=False
            )

            # merge with mergeid
            if len(df)==0:
                df = temp
            else:
                if 'mergeid' not in temp.columns:
                    st.write(f"mergeid not found in {file_name} (removed from the dataset)")
                else:
                    df = df.merge(
                        temp,
                        on='mergeid',
                        how='outer'
                    )

        df = df[cols]
        self.df = df
        return df
    

    def display_dataset_properties(self, df, key, print_na: bool = True):
        """
        Display the properties of the dataset.
        Args:
            - df: the dataset.
            - key: the key to use for the widgets.
            - print_na: whether to print the missing values.
        """

        make_space(2)

        # display the first rows of the dataset
        st.markdown("First rows of the dataset")
        st.write(df.head())
        make_space(2)

        # display statistics about the dataset
        st.markdown("Dataset shape")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.success(f"{df.shape[0]} rows and {df.shape[1]} columns")
        with col2:
            st.warning(f"Memory usage: {df.memory_usage().sum()/(1024*1024):.2f} MB")
        make_space(2)
        
        if print_na:

            st.markdown("Missing values")

            # count missing values
            missing_values = df.isna().sum()/df.shape[0]#*100
            missing_values = missing_values.to_frame('missing_values')
            missing_values['column'] = missing_values.index
            missing_values = missing_values.sort_values(by='missing_values', ascending=False)
            
            # display percentage of missing values per column
            c1, used_col, c3 = st.columns([1, 6, 1])
            with used_col:
                st.data_editor(
                    missing_values,
                    column_config={
                        "missing_values": st.column_config.ProgressColumn(
                            "% of missing values",
                            min_value=0,
                            max_value=1,
                            width='large'
                        ),
                    },
                    hide_index=True,
                    key=key
                )
    

    def replace_missing_codes(self, df: pd.DataFrame) -> pd.DataFrame:
        valuesToReplace = [
            "Don't know",
            "Refusal",
            "Implausible value/suspected wrong",
            "Not codable",
            "Not answered",
            "Not yet coded",
            "Not applicable",
            -9999991,
            -9999992,
        ]
        df = df.replace(valuesToReplace, pd.NA)
        self.df = df
        return df
    
    def make_explicit_na(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.fillna('missing')
        self.df = df
        return df
    
    def count_percent_na_columns(self, df: pd.DataFrame, threshold: int) -> pd.DataFrame:
        """
        Count the percentage of missing values in each column.
        Args:
            - df: the dataset.
            - threshold: the threshold to use.
        Returns:
            - cols_to_remove: the columns to remove.
        """
        missing_values = df.isna().sum()/df.shape[0] * 100
        cols_to_remove = missing_values[missing_values>threshold].index
        return cols_to_remove.to_list()