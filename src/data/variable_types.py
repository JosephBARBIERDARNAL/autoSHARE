"""
This module contains the VariableTypesManager class.
"""


class VariableTypesManager:
    """
    Class to handle the dataset.
    """

    def __init__(self):
        pass

    def get_variable_types(self, df):
        """
        Get the variable types of the columns in the dataset.
        """
        return df.dtypes
