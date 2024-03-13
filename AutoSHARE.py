import streamlit as st
import pandas as pd
from src.ui import make_space, loadHeader, loadFooter
from src.const import yearToWave, waveToYear, dataPath
from src.const import helpWave, helpColumns, helpTarget, helpPredictors


loadHeader(
    title="Auto SHARE",
    subtitle="Analyze and model the SHARE data with ease"
)
make_space(3)



# DEFINE WAVE
st.markdown("### Wave")
wave = st.selectbox(
    'Select a wave:',
    options=list(waveToYear.keys()),
    key=1,
    help=helpWave
)
wave = int(wave)
st.markdown(f"Selected wave: {wave}")
make_space(2)


if wave:

    # DEFINE VARIABLES
    st.markdown("### Variables")
    with open(f'static/columns/wave_{int(wave)}_columns.txt') as file:
        columns = file.read().splitlines()
    cols = st.multiselect(
        'Select the columns you want to load:',
        options=columns,
        key=2,
        help=helpColumns
    )
    if len(cols)>0:
        st.markdown(f"Selected columns:\n{cols}")
        make_space(2)


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





loadFooter()