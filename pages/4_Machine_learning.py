from json import load
import streamlit as st
from src.ui.ui import make_space, load_footer, load_header
from src.viz.plot import Plot
from src.ui.helps import (
      HELPTARGET,
      HELPPREDICTORS,
      HELPTASK,
      HELPFITEST,
   )

if "df" not in st.session_state:
   st.stop()

else:

   load_header(title="Machine Learning", subtitle="Modeling and prediction")
   make_space(10)

   df = st.session_state["df"]

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
   col_to_display = st.session_state["col_to_display"]
   display_to_col = st.session_state["display_to_col"]
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

load_footer()