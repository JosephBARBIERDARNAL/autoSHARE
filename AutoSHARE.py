import streamlit as st
from src.ui import make_space, loadHeader, loadFooter
from src.const import yearToWave, waveToYear, data_path
from src.const import helpWave, helpColumns, helpTarget, helpPredictors, helpExplicitNA, helpMissingCode, helpDropNA
from src.data import load_data_properties, datasetManager


loadHeader(
    title="Auto SHARE",
    subtitle="Analyze and model the SHARE data with ease"
)
make_space(10)




# DEFINE WAVE
st.markdown("### Wave")
wave = st.slider(
    'Select a wave:',
    min_value=1,
    max_value=8,
    value=1,
    key=1,
    help=helpWave
)
wave = int(wave)
year = waveToYear[wave]
st.markdown(f"Selected wave: {wave} ({year})")
make_space(10)


if wave:

    # DEFINE VARIABLES
    st.markdown("### Variables")
    columns_properties = load_data_properties(wave)
    columns = columns_properties['column'].tolist()
    cols = st.multiselect(
        'Select the columns you want to load:',
        options=columns,
        key=2,
        help=helpColumns
    )
    if len(cols)>0:

        col1, col2 = st.columns([1, 1])
        with col1:
            load_data = st.checkbox(
                "Load data (can take a while...)",
                value=False,
                key=5
            )
        if load_data:
            datasetManager = datasetManager(data_path, wave)
            df = datasetManager.create_dataframe(cols)
            with col2:
                display_properties = st.checkbox(
                    "Display dataset properties",
                    value=False,
                    key=6
                )
            if display_properties:
                datasetManager.display_dataset_properties(df)
            make_space(10)


            # MISSING VALUES MANAGEMENT
            st.markdown("### Missing values")
            na_before = df.isna().sum().sum()
            st.error(f"Number of missing values before: {na_before}")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                same_missing_code = st.checkbox(
                    'Consider all missing codes as NaN',
                    value=True,
                    key=9,
                    help=helpMissingCode
                )
            with col2:
                explicit_na = st.checkbox(
                    'Consider missing values as a separate category',
                    value=False,
                    key=7,
                    help=helpExplicitNA
                )
            with col3:
                drop_row_na = st.checkbox(
                    'Drop rows with missing values',
                    value=False,
                    key=8,
                    help=helpDropNA
                )
            
            if drop_row_na:
                df = df.dropna()
            if same_missing_code:
                df = datasetManager.replace_missing_codes(df)
            if explicit_na:
                df = datasetManager.make_explicit_na(df)

            na_after = df.isna().sum().sum()
            st.success(f"Number of missing values after: {na_after}")
            
            if display_properties:
                make_space(1)
                datasetManager.display_dataset_properties(df, print_na=False)








loadFooter()