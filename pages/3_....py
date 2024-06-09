import streamlit as st
from src.ui.ui import (
    make_space,
    load_header,
    load_footer
)

load_header(title="Other pages", subtitle="Other pages to be implemented")

make_space(3)
st.warning("This page would be used to display other pages that would be implemented in the future.")
st.markdown("""Some of the pages to be implemented include:  
- Data visualization with Plotly
- Hypothesis testing
- Bayesian statistics
- Other?
""")


make_space(10)
load_footer()