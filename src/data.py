import pandas as pd
import numpy as np
from scipy import stats
import streamlit as st

from src.utils import clean_suffix_from_cols, load_data_properties





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
        file_names.append(f'wave{self.wave}_dummy.stata')

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

        # add country and language
        cols.extend(['country', 'language'])

        # remove dupplicate columns from merging
        df = clean_suffix_from_cols(df)

        # keep only the selected columns
        cols = list(set(cols))
        df = df[cols]

        # output
        self.df = df
        return df
    
    

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
    

