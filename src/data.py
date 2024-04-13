import pandas as pd
import numpy as np
from scipy import stats
import streamlit as st
from src.ui import make_space



@st.cache_data(show_spinner=False)
def load_data_properties(wave: int, data_path: str = 'static/columns'):
    """
    Load the properties of the columns for the specified wave.
    """
    columns_properties = pd.read_csv(f'{data_path}/wave_{wave}_columns.csv')
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
    

    def display_dataset_properties(self, df: pd.DataFrame, key: str, print_na: bool = True):
        """
        Display the properties of the dataset.
        Args:
            - df: the dataset.
            - key: the key to use for the widgets.
            - print_na: whether to print the missing values.
        """

        make_space(2)

        # display the first rows of the dataset
        st.markdown("Preview of the dataset")
        st.write(df.head())        

        # display statistics about the dataset
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.success(f"{df.shape[0]} rows")
        with col2:
            st.warning(f"Memory usage: {df.memory_usage().sum()/(1024*1024):.2f} MB")
        with col3:
            st.download_button(
            label="Download dataset",
            data=df.to_csv(index=False),
            file_name=f"wave_{self.wave}_dataset.csv",
            mime="text/csv",
            key=key+"_download"
        )
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
    
    def find_z_outliers(self, threshold_z: int, df: pd.DataFrame):
        """
        Find outliers using the Z-score.
        Args:
            - threshold_z: the threshold to use.
            - df: the dataset.
        Returns:
            - outliers: the index of the outliers.
        """

        # normalize
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df_num = df[numerical_cols]
        df_num = (df_num - df_num.mean()) / df_num.std()

        # get index of outliers
        z = np.abs(stats.zscore(df_num))
        outliers = np.where(z > threshold_z)
        outliers = df.iloc[outliers[0]].index
        return outliers
    
    def find_iqr_outliers(self, threshold_iqr: float, df: pd.DataFrame):
        """
        Find outliers using the IQR.
        Args:
            - threshold_iqr: the threshold to use.
            - df: the dataset.
        Returns:
            - outliers: the index of the outliers.
        """
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
        Q1 = df[numerical_cols].quantile(0.25)
        Q3 = df[numerical_cols].quantile(0.75)
        IQR = Q3 - Q1
        lower_filter = (df[numerical_cols] < (Q1 - threshold_iqr * IQR))
        upper_filter = (df[numerical_cols] > (Q3 + threshold_iqr * IQR))
        outliers = df[(lower_filter | upper_filter).any(axis=1)].index
        return outliers
    
    def find_outliers(self, threshold: float, method: str, df: pd.DataFrame):

        if method not in ['Z-score', 'IQR', 'Isolation Forest']:
            raise ValueError("Method not supported.")
        
        if method=='Z-score':
            outliers = self.find_z_outliers(threshold, df)
        elif method=='IQR':
            outliers = self.find_iqr_outliers(threshold, df)
        return outliers

    def remove_outliers(self, index: list, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove the outliers.
        Args:
            - index: the index of the outliers.
            - df: the dataset.
        Returns:
            - df: the dataset without the outliers.
        """
        df = df.drop(index)
        self.df = df
        return df
    