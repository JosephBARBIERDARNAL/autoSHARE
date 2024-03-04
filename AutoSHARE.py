import streamlit as st
from src.ui import makeSpace, loadHeader, loadFooter
from src.const import yearToWave, waveToYear, helpWave, dataPath


loadHeader(
    title="Auto SHARE",
    subtitle="Analyze and model the SHARE data with ease"
)
makeSpace(3)


st.markdown("### Wave")
wave = st.selectbox(
    'Select a wave:',
    options=list(waveToYear.keys()),
    key=1,
    help=helpWave
)
st.markdown(f"Selected wave: {wave}")
makeSpace(2)







loadFooter()