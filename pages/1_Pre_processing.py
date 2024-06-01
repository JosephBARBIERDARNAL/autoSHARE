"""
Auto SHARE is a Streamlit app that allows users to load, clean, and analyze the SHARE data with ease
"""

import streamlit as st
import pandas as pd
import json

from src.ui.helps import (
    HELPCOLUMNS,
    HELPCOLUMNSNA,
    HELPEXPLICITNA,
    HELPMISSINGCODE,
    HELPDROPNA,
    HELPOUTLIERS,
    HELPZSCORE,
    HELPIQR,
    HELPWAVE,
    HELPNUMERICAL,
    HELPCATEGORICAL,
    HELPUPLOADCONFIG,
    HELPTARGET,
    HELPPREDICTORS,
    HELPTASK,
    HELPFITEST,
)
from src.constants import waveToYear
from src.utils import load_data_properties
from src.model.model import ModelManager
from src.data.data import DatasetManager
from src.data.outliers import OutliersManager
from src.data.missing_values import MissingValuesManager
from src.viz.plot import Plot
from src.ui.ui import (
    make_space,
    load_header,
    load_footer,
    display_meta,
    display_config_explanation,
)

DATA_PATH = "static/data"


load_header(title="Data pre processing", subtitle="Load, merge, clean, filter, and save the SHARE data")
make_space(10)


# DEFINE WAY TO USE APP
st.markdown("### Use with a config file")
with st.expander("Use the app with a config file"):
    st.markdown(
        """
    This section refers how to use the app if you already did once and want to apply
    the exact same configuration.

    If you already used this app before, you might have saved a `configAutoSHARE.json` file
    that contains all the settings you used. Here, you can decide to directly load
    it so you don't have to manually re-do everything. The app will automatically
    use the settings in the file and apply the same steps.
    """
    )
    use_my_config = st.toggle("Use my config file")
    if use_my_config:

        # get config file
        config_file = st.file_uploader(
            "Upload configAutoSHARE.json",
            type="json",
            accept_multiple_files=False,
            key="upload_config",
            help=HELPUPLOADCONFIG,
        )
        if config_file:
            try:
                config = json.load(config_file)
                wave = config["wave"]
                year = config["year"]
                cols = config["columns"]
                same_missing_code = config["same_missing_code"]
                explicit_na = config["explicit_na"]
                drop_row_na = config["drop_row_na"]
                remove_cols_na = config["remove_cols_na"]
                threshold = config["threshold"]
                remove_outliers = config["remove_outliers"]
                variables = config["variables"]
                method = config["method"]
                threshold = config["threshold"]
                target = config["target"]
                predictors = config["predictors"]
                task = config["task"]
                model = config["model"]
            except KeyError as e:
                st.error(
                    f"""Error: config file is missing the following keys: {e}.
                Make sure that you didn't modify the file manually."""
                )
                st.stop()
            st.success("Config file loaded successfully!")
            successfully_loaded = True

            # display configuration
            display_config = st.toggle("Display configuration")
            if display_config:
                st.write(config)
        else:
            successfully_loaded = False


##################################################################################
####### APP WITH CONFIG FILE #####################################################
##################################################################################

if use_my_config and successfully_loaded == True:

    # init managers
    DatasetManager = DatasetManager(DATA_PATH, wave)
    OutliersManager = OutliersManager()
    MissingValuesManager = MissingValuesManager()
    ModelManager = ModelManager()

    # run app with config file
    df = DatasetManager.create_dataframe(cols)
    if drop_row_na:
        df = df.dropna()
    if same_missing_code:
        df = MissingValuesManager.replace_missing_codes(df)
    if explicit_na:
        df = MissingValuesManager.make_explicit_na(df)
    if remove_cols_na:
        cols_to_remove = MissingValuesManager.remove_na_columns(df, threshold)
        df = df.drop(columns=cols_to_remove)
    if remove_outliers:
        outliers = OutliersManager.find_outliers(threshold, method, df)
        df = OutliersManager.remove_outliers(outliers, df)
    model = ModelManager.fit_model(df[predictors], df[target], model)
    summary_table = ModelManager.display_model()
    st.write(summary_table)

    col1, col2 = st.columns([1, 1])
    with col1:

        # save summary table as csv
        summary_table_csv = summary_table.as_csv()
        st.download_button(
            label="Download model summary as CSV",
            data=summary_table_csv,
            file_name="model_summary.csv",
            mime="text/csv",
        )
    with col2:

        # download dataset
        st.download_button(
            label="Download dataset as CSV",
            data=df.to_csv(index=False),
            file_name=f"share_dataset.csv",
            mime="text/csv",
        )


##################################################################################
####### APP WITHOUT CONFIG FILE ##################################################
##################################################################################

elif not use_my_config:

    # DEFINE WAVE
    make_space(10)
    st.markdown("### Wave")
    wave = st.slider(
        "Select a wave:", min_value=1, max_value=9, value=1, key="wave", help=HELPWAVE
    )
    wave = int(wave)
    year = waveToYear[wave]
    st.markdown(f"Selected wave: {wave} ({year})")
    make_space(10)

    # init managers
    DatasetManager = DatasetManager(DATA_PATH, wave)
    OutliersManager = OutliersManager()
    MissingValuesManager = MissingValuesManager()

    # DEFINE VARIABLES
    st.markdown("### Variables")
    columns_properties = load_data_properties(wave)
    columns = columns_properties["column"].tolist()
    columns = sorted(columns)
    labels = columns_properties["labels"].tolist()
    display_options = [f"{col} ({label})" for col, label in zip(columns, labels)]
    display_options = sorted(display_options)
    display_to_col = {display: col for display, col in zip(display_options, columns)}
    col_to_display = {col: display for display, col in zip(display_options, columns)}
    cols_selected_display = st.multiselect(
        "Select the columns you want to load:",
        options=display_options,
        key="columns",
        max_selections=10,
        help=HELPCOLUMNS,
    )
    cols = [display_to_col[col] for col in cols_selected_display]
    if len(cols) > 0:

        # load dataframe with chosen columns
        load_data = st.toggle("Load data", value=False, key="load_data")
        if load_data:
            df = DatasetManager.create_dataframe(cols)
            display_meta(df, key="dataset_info variables")
            make_space(10)

            # DEFINE VARIABLE TYPES
            st.markdown("### Variable types")
            col1, col2 = st.columns([1, 1])
            with col1:
                numerical_columns = st.multiselect(
                    "Select the numerical columns:",
                    options=df.columns.tolist(),
                    key="numerical",
                    help=HELPNUMERICAL,
                )
            with col2:
                categorical_columns = st.multiselect(
                    "Select the categorical columns:",
                    options=df.columns.tolist(),
                    key="categorical",
                    help=HELPCATEGORICAL,
                )
            if len(numerical_columns) + len(categorical_columns) != len(df.columns):
                st.error(
                    f"The number of numerical ({len(numerical_columns)}) and categorical ({len(categorical_columns)}) \
                    columns does not match the total number of columns {len(df.columns)}."
                )
            elif len(set(numerical_columns).intersection(categorical_columns)) > 0:
                st.error(
                    f"Variable(s) {set(numerical_columns).intersection(categorical_columns)} are present in both lists."
                )
            else:
                st.success("Variables types defined successfully!")
                df[numerical_columns] = df[numerical_columns].astype("float")
                df[categorical_columns] = df[categorical_columns].astype("category")
                st.write(df.dtypes)
                make_space(3)
                display_meta(df, key="dataset_info dtypes", print_na=False)
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
                        help=HELPMISSINGCODE,
                    )
                with col2:
                    explicit_na = st.toggle(
                        "Consider missing values as a separate category",
                        value=False,
                        key="explicit_na",
                        help=HELPEXPLICITNA,
                    )
                with col3:
                    drop_row_na = st.toggle(
                        "Drop rows with missing values",
                        value=False,
                        key="drop_row_na",
                        help=HELPDROPNA,
                    )

                nrows_df_before = df.shape[0]
                if same_missing_code:
                    df = MissingValuesManager.replace_missing_codes(df)
                    
                    # for some reason, this step changes the dtypes of the columns
                    df[numerical_columns] = df[numerical_columns].astype("float")
                    df[categorical_columns] = df[categorical_columns].astype("category")
                if explicit_na:
                    df = MissingValuesManager.make_explicit_na(df)
                if drop_row_na:
                    df.dropna(inplace=True)
                nrows_df_after = df.shape[0]
                st.warning(
                    f"Number of rows removed: {nrows_df_before - nrows_df_after} \
                    ({(nrows_df_before - nrows_df_after) / nrows_df_before:.2%} of the dataset)"
                )

                make_space(3)

                remove_cols_na = st.toggle(
                    "Remove columns based on missing values",
                    value=False,
                    key="remove_cols_na",
                    help=HELPCOLUMNSNA,
                )
                if remove_cols_na:
                    threshold = st.slider(
                        "Select the threshold for missing values:",
                        min_value=0,
                        max_value=100,
                        value=90,
                        key="threshold",
                    )
                    cols_to_remove = MissingValuesManager.remove_na_columns(df, threshold)
                    if len(cols_to_remove) > 0:
                        st.markdown(
                            f"Columns removed (with threshold of {threshold}%): `{', '.join(cols_to_remove)}`"
                        )
                        df.drop(columns=cols_to_remove, inplace=True)

                make_space(3)
                na_after = df.isna().sum().sum()
                display_meta(df, key="dataset_info missing")
                make_space(10)

                # OUTLIERS MANAGEMENT
                if na_after == 0:
                    st.markdown("### Outliers")
                    remove_outliers = st.toggle(
                        "Remove outliers",
                        value=False,
                        key="remove_outliers",
                        help=HELPOUTLIERS,
                    )

                    if remove_outliers:

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
                                help=HELPZSCORE,
                            )

                        elif method == "IQR":
                            threshold = st.slider(
                                "Select the threshold for IQR:",
                                min_value=0.0,
                                max_value=10.0,
                                step=0.1,
                                value=1.5,
                                key="threshold_iqr",
                                help=HELPIQR,
                            )

                        elif method == "Isolation Forest":
                            outliers = []
                            st.error(
                                "Method not implemented yet. Will use Z-score (z=3) instead."
                            )
                            method, threshold = "Z-score", 3.0

                        outliers = OutliersManager.find_outliers(threshold, method, df, numerical_columns)
                        n_outliers = len(outliers)
                        prop_outliers = n_outliers / df.shape[0]
                        st.warning(
                            f"Number of outliers removed: {n_outliers} ({prop_outliers:.2%} of the dataset)"
                        )
                        df = OutliersManager.remove_outliers(outliers, df)

                        make_space(3)
                        display_meta(df, key="dataset_info outliers", print_na=False)
                    else:
                        variables = df.columns.tolist()
                        method = "None"
                        threshold = 0.0
                    make_space(10)

                    # MODELING
                    st.markdown("### Target and predictors selection")
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        target = st.selectbox(
                            "Select the target variable:",
                            options=df.columns.tolist(),
                            key="target",
                            help=HELPTARGET,
                        )
                    with col2:
                        predictors = st.multiselect(
                            "Select the predictor variables:",
                            options=df.columns.tolist(),
                            key="predictors",
                            help=HELPPREDICTORS,
                        )

                    # check if target is in predictors
                    if target in predictors:
                        st.warning(
                            """The *target variable* is currently in the *predictor variables*.
                        This can lead to various **numerical issues**. It is recommended to **remove** it."""
                        )

                    make_space(3)
                    cols_for_model = [target] + predictors
                    cols_model_display = [col_to_display[col] for col in cols_for_model]
                    st.write(f"Columns for modeling: `{', '.join(cols_for_model)}`")
                    with st.expander("Visualize data distribution"):
                        col_to_plot = st.selectbox(
                            "Select the column to plot:",
                            options=cols_model_display,
                            key="column_plot",
                        )
                        col_to_plot = display_to_col[col_to_plot]
                        Plot().distribution(df, col_to_plot)

                    make_space(10)

                    # MODELING
                    st.markdown("### Modeling")
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        task = st.selectbox(
                            "Select the task:",
                            options=["Classification", "Regression"],
                            help=HELPTASK,
                            key="task",
                        )
                    with col2:
                        if task == "Classification":
                            available_models = ["Logistic Regression"]
                        elif task == "Regression":
                            available_models = ["Linear Regression"]

                        model = st.selectbox(
                            "Select the model:",
                            options=available_models,
                            key="model",
                        )

                    fit_estimator = st.toggle(
                        "Fit the model", value=False, help=HELPFITEST, key="fit_estimator"
                    )

                    if fit_estimator:
                        ModelManager = ModelManager()
                        model_fit = ModelManager.fit_model(
                            df[predictors], df[target], model
                        )
                        summary_table = ModelManager.display_model()
                        st.write(summary_table)

                        # save summary table as csv
                        summary_table_csv = summary_table.as_csv()
                        st.download_button(
                            label="Download model summary as CSV",
                            data=summary_table_csv,
                            file_name="model_summary.csv",
                            mime="text/csv",
                        )

                        can_display_config = True

                        # SAVE CONFIGURATION (create json file with all the configurations)
                        if can_display_config:
                            make_space(10)
                            display_config_explanation(
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
                            )


load_footer()
