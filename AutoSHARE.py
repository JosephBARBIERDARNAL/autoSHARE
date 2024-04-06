import streamlit as st
from src.ui import make_space, load_header, load_footer
from src.const import *
from src.data import load_data_properties, datasetManager



load_header(
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
    key='wave',
    help=helpWave
)
wave = int(wave)
year = waveToYear[wave]
st.markdown(f"Selected wave: {wave} ({year})")
make_space(10)


# DEFINE VARIABLES
st.markdown("### Variables")
columns_properties = load_data_properties(wave)
columns = columns_properties['column'].tolist()
cols = st.multiselect(
    'Select the columns you want to load:',
    options=columns,
    key='columns',
    help=helpColumns
)
if len(cols)>0:

    load_data = st.toggle(
        "Load data",
        value=False,
        key='load_data'
    )
    if load_data:
        datasetManager = datasetManager(data_path, wave)
        df = datasetManager.create_dataframe(cols)
        with st.expander("Dataset info"):
            datasetManager.display_dataset_properties(df, key='dataset_info variables')
        make_space(10)


        # MISSING VALUES MANAGEMENT
        st.markdown("### Missing values")
        na_before = df.isna().sum().sum()
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            same_missing_code = st.toggle(
                'Consider all missing codes as NA',
                value=True,
                key='same_missing_code',
                help=helpMissingCode
            )
        with col2:
            explicit_na = st.toggle(
                'Consider missing values as a separate category',
                value=False,
                key='explicit_na',
                help=helpExplicitNA
            )
        with col3:
            drop_row_na = st.toggle(
                'Drop rows with missing values',
                value=False,
                key='drop_row_na',
                help=helpDropNA
            )
        
        if drop_row_na:
            df = df.dropna()
        if same_missing_code:
            df = datasetManager.replace_missing_codes(df)
        if explicit_na:
            df = datasetManager.make_explicit_na(df)

        make_space(3)

        remove_cols_na = st.toggle(
            'Remove columns based on missing values',
            value=False,
            key='remove_cols_na',
            help=helpColumnsNA
        )
        if remove_cols_na:
            threshold = st.slider(
                'Select the threshold for missing values:',
                min_value=0,
                max_value=100,
                value=90,
                key='threshold'
            )
            cols_to_remove = datasetManager.count_percent_na_columns(df, threshold)
            st.write(f"Columns removed: {cols_to_remove}")
            df = df.drop(columns=cols_to_remove)
        
        
        make_space(3)
        na_after = df.isna().sum().sum()
        with st.expander("Dataset info"):
            datasetManager.display_dataset_properties(df, key='dataset_info missing')








load_footer()