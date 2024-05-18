import streamlit as st
import pandas as pd
from openai import OpenAI, BadRequestError

from src.ui.ui import load_footer
from pages.ChereDoc.utils import extract_content, call_gpt, space

client = OpenAI(api_key=st.secrets["api_key"])

# load the questionnaire
df = pd.read_csv("pages/ChereDoc/doc.csv")

st.title("ChereDoc: from question id to question")
st.markdown(
    "##### This web page is a tool to find the question corresponding to a question id in the [SHARE](https://share-eric.eu/) Survey. To use it, choose a wave and a question id, then click on `Run`. For the moment, the app only covers English questionnaires from the waves 1 to 8."
)
st.markdown(
    "##### Our app get all columns from the datasets and search in the documentation to find the question corresponding to the question id. However, not all columns are explicit questions: most valid questions have the form `ab012_`."
)
space(2)

# init the columns
col1, col2 = st.columns(2)


# get the right wave questionnaire
with col1:
    wave_number = st.selectbox(
        "Choose a wave", ["Wave " + str(val) for val in range(1, 9)], key="wave_number"
    )
    wave_number = wave_number[-1]
    wave_name = f"w{wave_number}_main_en.pdf"
    wave_quest = df[df["name"] == wave_name]["text"]
    wave_quest = wave_quest.values[0]

# get the question id
with col2:
    column_names = []
    with open(
        f"pages/ChereDoc/column_names/column_names_wave{wave_number}.txt", "r"
    ) as file:
        for line in file:
            column_names.append(line.strip())
    question_id = st.selectbox("Choose a question id", column_names, key="question_id")

    # keep ony 5 first letters
    if len(question_id) in [6, 7]:
        question_id = question_id[:5]

# get run validation
run = st.button("Run")
if run:
    with st.spinner("Searching..."):

        # find the part correspond to the question id in the questionnaire
        content = extract_content(question_id, wave_quest)

        # ask gpt to find the question in text
        try:
            question_found = call_gpt(client, content)
            st.success(question_found)
        except BadRequestError:
            st.error("Question not found")


load_footer()
