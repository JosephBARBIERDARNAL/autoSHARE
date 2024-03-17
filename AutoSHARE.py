import streamlit as st
from src.ui import make_space, loadHeader, loadFooter
from src.const import yearToWave, waveToYear, data_path
from src.const import helpWave, helpColumns, helpTarget, helpPredictors, helpExplicitNA, helpMissingCode
from src.data import load_data_properties, datasetManager


loadHeader(
    title="Auto SHARE",
    subtitle="Analyze and model the SHARE data with ease"
)
make_space(8)




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
make_space(8)


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
        st.markdown(f"Selected columns:\n{cols}")
        make_space(8)


        # DEFINE TARGET AND PREDICTORS
        st.markdown("### Predictors and Target")
        col1, col2 = st.columns([1,3])
        with col1:
            target = st.selectbox(
                'Select the target variable:',
                options=cols,
                key=3,
                help=helpTarget
            )
            st.markdown(f"Selected target: {target}")
        with col2:
            predictors = st.multiselect(
                'Select the predictor variables:',
                options=cols,
                key=4,
                help=helpPredictors
            )
            st.markdown(f"Selected predictors: {predictors}")


        # CREATE DATASET
        if len(predictors)>0 and target:
            make_space(8)
            st.markdown("### Data")
            load_data = st.checkbox(
                "Load data (can take a while...)",
                value=False,
                key=5
            )
            if load_data:
                datasetManager = datasetManager(data_path, wave)
                df = datasetManager.create_dataframe(cols)
                datasetManager.display_dataset_properties(df)
                make_space(8)


                # DEFINE MODEL
                st.markdown("### Missing values")
                same_missing_code = st.checkbox(
                    'Consider all missing codes as NaN',
                    value=True,
                    key=6,
                    help=helpMissingCode
                )
                explicit_na = st.checkbox(
                    'Consider missing values as a separate category',
                    value=False,
                    key=7,
                    help=helpExplicitNA
                )








loadFooter()