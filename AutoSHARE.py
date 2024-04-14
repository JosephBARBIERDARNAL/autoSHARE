import streamlit as st

from src.const import *
from src.utils import load_data_properties
from src.data import DatasetManager
from src.outliers import OutliersManager
from src.missing_values import MissingValuesManager
from src.ui import make_space, load_header, load_footer, display_meta


load_header(title="Auto SHARE", subtitle="Analyze and model the SHARE data with ease")
make_space(10)


# DEFINE WAVE
st.markdown("### Wave")
wave = st.slider(
    "Select a wave:", min_value=1, max_value=9, value=1, key="wave", help=helpWave
)
wave = int(wave)
year = waveToYear[wave]
st.markdown(f"Selected wave: {wave} ({year})")
make_space(10)


# init managers
DatasetManager = DatasetManager(data_path, wave)
OutliersManager = OutliersManager()
MissingValuesManager = MissingValuesManager()


# DEFINE VARIABLES
st.markdown("### Variables")
columns_properties = load_data_properties(wave)
columns = columns_properties["column"].tolist()
cols = st.multiselect(
    "Select the columns you want to load:",
    options=columns,
    key="columns",
    max_selections=10,
    help=helpColumns,
)
if len(cols) > 0:

    # load dataframe with chosen columns
    load_data = st.toggle("Load data", value=False, key="load_data")
    if load_data:
        df = DatasetManager.create_dataframe(cols)
        display_meta(df, key="dataset_info variables")
        make_space(10)

        # MISSING VALUES MANAGEMENT
        st.markdown("### Missing values")
        na_before = df.isna().sum().sum()
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            same_missing_code = st.toggle(
                "Consider all missing codes as NA",
                value=False,
                key="same_missing_code",
                help=helpMissingCode,
            )
        with col2:
            explicit_na = st.toggle(
                "Consider missing values as a separate category",
                value=False,
                key="explicit_na",
                help=helpExplicitNA,
            )
        with col3:
            drop_row_na = st.toggle(
                "Drop rows with missing values",
                value=False,
                key="drop_row_na",
                help=helpDropNA,
            )

        if drop_row_na:
            df = df.dropna()
        if same_missing_code:
            df = MissingValuesManager.replace_missing_codes(df)
        if explicit_na:
            df = MissingValuesManager.make_explicit_na(df)

        make_space(3)

        remove_cols_na = st.toggle(
            "Remove columns based on missing values",
            value=False,
            key="remove_cols_na",
            help=helpColumnsNA,
        )
        if remove_cols_na:
            threshold = st.slider(
                "Select the threshold for missing values:",
                min_value=0,
                max_value=100,
                value=90,
                key="threshold",
            )
            cols_to_remove = MissingValuesManager.count_na_columns(df, threshold)
            st.write(f"Columns removed: {cols_to_remove}")
            df = df.drop(columns=cols_to_remove)

        make_space(3)
        na_after = df.isna().sum().sum()
        display_meta(df, key="dataset_info missing")
        make_space(10)

        # OUTLIERS MANAGEMENT
        st.markdown("### Outliers")
        remove_outliers = st.toggle(
            "Remove outliers", value=False, key="remove_outliers", help=helpOutliers
        )

        if remove_outliers:

            col1, col2 = st.columns([1, 1])
            with col1:
                # choose variables to apply the method
                variables = df.columns.tolist()
                variables = st.multiselect(
                    "Select the variables to apply the method:",
                    options=variables,
                    key="variables outliers",
                )
            with col2:
                # choose the method
                methods = ["Z-score", "IQR", "Isolation Forest"]
                method = st.selectbox(
                    "Select the method to remove outliers:",
                    options=methods,
                    key="method outliers",
                )

            if method == "Z-score":
                threshold = st.slider(
                    "Select the threshold for Z-score:",
                    min_value=0.0,
                    max_value=10.0,
                    step=0.1,
                    value=3.0,
                    key="threshold_z",
                    help=helpZScore,
                )

            elif method == "IQR":
                threshold = st.slider(
                    "Select the threshold for IQR:",
                    min_value=0.0,
                    max_value=10.0,
                    step=0.1,
                    value=1.5,
                    key="threshold_iqr",
                    help=helpIQR,
                )

            elif method == "Isolation Forest":
                outliers = []
                st.error("Method not implemented yet. Will use Z-score (z=3) instead.")
                method, threshold = "Z-score", 3.0

            outliers = OutliersManager.find_outliers(threshold, method, df)
            n_outliers = len(outliers)
            prop_outliers = n_outliers / df.shape[0]
            st.warning(
                f"Number of outliers removed: {n_outliers} ({prop_outliers:.2%} of the dataset)"
            )
            df = OutliersManager.remove_outliers(outliers, df)

            make_space(3)
            display_meta(df, key="dataset_info outliers", print_na=False)
            make_space(10)


load_footer()
