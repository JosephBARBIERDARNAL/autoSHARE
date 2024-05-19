"""
This module contains the OutliersManager class.
"""

import pandas as pd
import numpy as np
from scipy import stats

AVAILABLE_METHODS = ["Z-score", "IQR", "Isolation Forest"]

class OutliersManager:
    """
    The `OutliersManager` is a class to handle outliers
    in the dataset.
    """

    def __init__(self):
        self.outliers = []
        self.available_methods = AVAILABLE_METHODS

    def find_z_outliers(
        self,
        threshold_z: int,
        df: pd.DataFrame,
        numerical_cols: list
    ) -> list:
        """
        Find outliers using the Z-score.

        Args:

        - threshold_z: the threshold to use
        - df: the dataset
        - numerical_cols: the numerical columns

        Returns:

        - outliers: the index of the outliers
        """

        # normalize
        df_num = df[numerical_cols]
        df_num = (df_num - df_num.mean()) / df_num.std()

        # get index of outliers
        z = np.abs(stats.zscore(df_num))
        outliers = np.where(z > threshold_z)
        outliers = df.iloc[outliers[0]].index
        return outliers

    def find_iqr_outliers(
        self,
        threshold_iqr: float,
        df: pd.DataFrame,
        numerical_cols: list
    ) -> list:
        """
        Find outliers using the IQR.

        Args:

        - threshold_iqr: the threshold to use
        - df: the dataset
        - numerical_cols: the numerical columns
        
        Returns:

        - outliers: the index of the outliers
        """
        
        # define the IQR
        Q1 = df[numerical_cols].quantile(0.25)
        Q3 = df[numerical_cols].quantile(0.75)
        IQR = Q3 - Q1

        # get index of outliers
        lower_filter = df[numerical_cols] < (Q1 - threshold_iqr * IQR)
        upper_filter = df[numerical_cols] > (Q3 + threshold_iqr * IQR)
        outliers = df[(lower_filter | upper_filter).any(axis=1)].index
        return outliers

    def find_outliers(
        self,
        threshold: float,
        method: str,
        df: pd.DataFrame,
        numerical_cols: list
    ) -> list:
        """
        Find outliers using the specified method and threshold.

        Args:

        - threshold: the threshold to use
        - method: the method to use
        - df: the dataset
        - numerical_cols: the numerical columns

        Returns:

        - outliers: the index of the outliers
        """

        # check if method is supported
        if method not in self.available_methods:
            raise ValueError("Method not supported.")

        # find outliers
        if method == "Z-score":
            outliers = self.find_z_outliers(threshold, df, numerical_cols)
        elif method == "IQR":
            outliers = self.find_iqr_outliers(threshold, df, numerical_cols)
        self.outliers = outliers
        return outliers

    def remove_outliers(
        self,
        index: list,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Remove the outliers.

        Args:

        - index: the index of the outliers
        - df: the dataset

        Returns:

        - df: the dataset without the outliers
        """
        df = df.drop(index)
        return df
