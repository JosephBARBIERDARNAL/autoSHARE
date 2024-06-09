import streamlit as st
from src.ui.ui import (
    make_space,
    load_header,
    load_footer
)

load_header(title="Descriptive statistics", subtitle="Get descriptive statistics for the dataset")

make_space(3)
st.warning("This page would be used to display descriptive statistics for the dataset.")


make_space(10)
load_footer()