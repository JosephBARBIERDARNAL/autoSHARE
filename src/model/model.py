"""
This module contains the ModelManager class.
"""

import statsmodels.api as sm
import streamlit as st


class ModelManager:
    """
    Class to handle the model.
    """

    def __init__(self):
        self.str_to_func = {
            "Linear Regression": sm.WLS,
            "Logistic Regression": sm.GLM,
        }

    def fit_model(self, X, y, model):
        """
        Fit a model to the data.
        Args:
            X (DataFrame): the features.
            y (Series): the target.
            model (str): the model to fit.
        Returns:
            model_fitted: the fitted model.
        """

        self.model = model

        # add constant to the features
        X = sm.add_constant(X)

        # get the model function
        model = self.str_to_func[model]

        # if the model is logistic regression, specify the family
        if model == sm.GLM:
            model = model(y, X, family=sm.families.Binomial())
        else:
            model = model(y, X)

        # fit the model
        model_fitted = model.fit()

        self.model_fitted = model_fitted
        return model_fitted

    def display_model(self):
        """
        Display the model summary.
        Returns:
            str: the model summary.
        """
        return self.model_fitted.summary()
