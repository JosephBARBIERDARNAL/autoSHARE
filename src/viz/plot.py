"""
This module contains the Plot class.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


class Plot:
    """
    The `Plot` class is used to handle the plots.
    """

    def __init__(self):
        pass

    def distribution(
        self,
        df: pd.DataFrame,
        column: str,
        color: str="#FF4B4B"
    ):
        """
        Plot the distribution of a variable depending on its type.

        Args:

        - df: the dataset
        - column: the column to plot

        Returns:

        - fig: the plotly figure
        """

        # find the type of the column
        type = self.find_type(df, column)

        # bar plot for categorical variables
        if type == "categorical":

            # sort the values by count
            df[column] = df[column].sort_values()

            # create the figure
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=df[column].value_counts().index,
                        y=df[column].value_counts().values / len(df) * 100,
                        marker_color=color,
                    )
                ]
            )

        # histogram for numerical variables
        elif type == "numerical":

            # define number of bins
            bins = st.slider("Number of bins", 1, 100, 20)

            # create the figure
            fig = go.Figure(
                data=[
                    go.Histogram(
                        x=df[column],
                        nbinsx=bins,
                        marker_color=color,
                    )
                ]
            )

        # display the plot and return the figure
        st.markdown(f"Distribution of {column} (conisdered as a {type} variable)")
        st.plotly_chart(fig, use_container_width=True, help="distribution")
        return fig

    def find_type(
        self,
        df: pd.DataFrame,
        column: str
    ):
        """
        Find the type of a column.

        Args:

        - df: the dataset
        - column: the column to find the type of

        Returns:

        - type: the type of the column
        """
        if df[column].dtype == "object":
            return "categorical"
        else:
            return "numerical"
