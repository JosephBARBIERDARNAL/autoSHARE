import streamlit as st
import pandas as pd
import json


def make_space(n: int, sidebar: bool = False):
    """
    Inserts n empty lines in the UI.
    """

    for _ in range(n):
        if sidebar:
            st.sidebar.text("")
        else:
            st.text("")


def horizontal_line():
    """
    Inserts an horizontal line in the UI.
    """

    st.markdown("<hr>", unsafe_allow_html=True)


def load_header(title: str, subtitle: str):
    """
    Loads the header of the app.
    """
    st.html(f"<h1 style='text-align: center;'>{title}</h1>")
    st.html(f"<h4 style='text-align: center;'>{subtitle}</h1>")


def load_footer():
    """
    Loads the footer of the app.
    """
    make_space(15)

    css = """
    <style>
        h5 {
            text-decoration: none;
            text-align: center;
            color: #808080;
        }

        h5 a {
            color: red;
            text-decoration: none;
            transition: color 0.3s;
        }

        h5 a:hover {
            color: orange;
            text-decoration: none;
        }
    </style>
    """
    st.html(css)

    footer = f"""
    ##### Report bug, contribute or contact [here](https://github.com/JosephBARBIERDARNAL/autoSHARE)
    ##### Developed by [CIERI Analytics](https://www.cieri-analytics.com/)
    """
    st.markdown(footer)


def display_meta(df, key, print_na: bool = True):
    """
    Display the properties of the dataset.
    Args:
        - df: the dataset.
        - key: the key to use for the widgets. See Streamlit documentation.
        - print_na: whether to print the info about missing values.
    """

    with st.expander("Dataset info"):
        make_space(2)

        # display the first rows of the dataset
        st.markdown("Preview of the dataset")
        st.write(df.head(10))

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
                file_name=f"share_dataset.csv",
                mime="text/csv",
                key=key + "_download",
            )
        make_space(2)

        if print_na:

            st.markdown("Missing values")

            # count missing values
            missing_values = df.isna().sum() / df.shape[0]
            missing_values = missing_values.to_frame("missing_values")
            missing_values["column"] = missing_values.index
            missing_values = missing_values.sort_values(
                by="missing_values", ascending=False
            )

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
                            width="large",
                        ),
                    },
                    hide_index=True,
                    key=key,
                )


def display_config_explanation(
    wave,
    year,
    cols,
    same_missing_code,
    explicit_na,
    drop_row_na,
    remove_cols_na,
    remove_outliers,
    variables,
    method,
    threshold,
    df,
    target,
    predictors,
    task,
    model,
):
    st.markdown("### Configuration")
    with st.expander("What is this?"):
        st.markdown(
            """The configuration file will store all the **parameters**
            used in the data cleaning/modelling process. It's an easy way to keep track
            of the steps taken. Also, it can be used to
            reproduce the same cleaning/modelling process in the future and by so
            ensure **reproducibility**."""
        )
    config = {
        "wave": wave,
        "year": year,
        "columns": cols,
        "same_missing_code": same_missing_code,
        "explicit_na": explicit_na,
        "drop_row_na": drop_row_na,
        "remove_cols_na": remove_cols_na,
        "threshold": threshold,
        "remove_outliers": remove_outliers,
        "variables": variables,
        "method": method,
        "threshold": threshold,
        "target": target,
        "predictors": predictors,
        "task": task,
        "model": model,
    }
    today = pd.Timestamp.today().strftime("%Y_%m_%d_%Hh_%Mmin")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.download_button(
            label="Download configuration",
            data=json.dumps(config),
            file_name=f"configAutoSHARE_{today}.json",
            key="download_config",
        )
    with col2:
        st.download_button(
            label="Download dataset as CSV",
            data=df.to_csv(index=False),
            file_name=f"autoshare_data_{today}.csv",
            key="download_cleaned_data",
        )
