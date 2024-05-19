import pytest
import pandas as pd
from unittest.mock import patch
from src.viz.plot import Plot


df_categorical = pd.DataFrame({"Category": ["apple", "banana", "apple", "orange"]})
df_numerical = pd.DataFrame({"Value": [10, 15, 10, 20]})


@pytest.fixture
def plot_dist():
    return Plot()


def test_find_type_categorical(plot_dist):
    assert plot_dist.find_type(df_categorical, "Category") == "categorical"


def test_find_type_numerical(plot_dist):
    assert plot_dist.find_type(df_numerical, "Value") == "numerical"


@patch("streamlit.slider", return_value=20)
@patch("streamlit.plotly_chart")
@patch("streamlit.markdown")
def test_plot_distribution_categorical(
    mock_markdown, mock_plotly_chart, mock_slider, plot_dist
):
    fig = plot_dist.distribution(df_categorical, "Category")
    assert "Bar" in str(fig.data[0]), "Should use a bar plot for categorical data"


@patch("streamlit.slider", return_value=20)
@patch("streamlit.plotly_chart")
@patch("streamlit.markdown")
def test_plot_distribution_numerical(
    mock_markdown, mock_plotly_chart, mock_slider, plot_dist
):
    fig = plot_dist.distribution(df_numerical, "Value")
    assert "Histogram" in str(fig.data[0]), "Should use a histogram for numerical data"
