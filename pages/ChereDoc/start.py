from utils import *
import pandas as pd
import os

df = pd.DataFrame(columns=["text", "name"])
path = "pages/ChereDoc/doc/"

for file_name in os.listdir(path):
    if file_name.endswith(".pdf"):
        file_path = path + file_name

        # read and clean text
        text = read_pdf(file_path)
        text = clean_text(text)

        # add to dataframe
        temp_df = pd.DataFrame([[text, file_name]], columns=["text", "name"])
        df = pd.concat([df, temp_df])
        print(file_name)
print("\n Done!")

# reset index and save
df.index = range(len(df))
df.to_csv(f"{path}doc2.csv", index=False)
