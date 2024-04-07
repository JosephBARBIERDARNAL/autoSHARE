# Auto SHARE

### Analyze and model the SHARE data with ease

<br>
Run the project:

```
pip install -r requirements.txt
streamlit run AutoSHARE.py
```

<br><br><br><br><br><br><br><br><br><br><br><br><br>


### To add later

```
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
        default=cols,
        key=4,
        help=helpPredictors
    )
    st.markdown(f"Selected predictors: {predictors}")
```
