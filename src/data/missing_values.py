"""
This module contains the MissingValuesManager class.
"""

import pandas as pd


class MissingValuesManager:
    """
    Class to handle missing values.
    """

    def __init__(self):
        self.missing_values = []

    def replace_missing_codes(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Replace the missing codes with NA.
        Missing codes are different values, defined by SHARE, that
        are similar to missing values but can be used for specific
        purposes.

        Args:
            - df: the dataset

        Returns:
            - df: the dataset with missing codes replaced by NA
        """

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
        return df.replace(valuesToReplace, None)

    def make_explicit_na(
        self,
        df: pd.DataFrame,
        explicit_name: str="missing"
    ) -> pd.DataFrame:
        """
        Takes all missing values and replace them with an explicit name,
        also known as explicit missing values.

        Args:
            - df: the dataset
            - explicit_name: the name to use for the explicit missing values

        Returns:
            - df: the dataset with explicit missing values
        """
        return df.fillna(explicit_name)

    def count_na_columns(
        self,
        df: pd.DataFrame,
        threshold: int
    ) -> pd.DataFrame:
        """
        Count the percentage of missing values in each column

        Args:
            - df: the dataset
            - threshold: the threshold to use
        
        Returns:
            - cols_to_remove: the columns to remove
        """

        missing_values = df.isna().sum() / df.shape[0] * 100
        cols_to_remove = missing_values[missing_values > threshold].index
        return cols_to_remove.to_list()
