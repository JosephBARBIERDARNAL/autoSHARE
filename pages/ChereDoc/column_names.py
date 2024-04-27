import pandas as pd
import os


def save_column_names(directory, wave):

    distinct_columns = set()

    # Iterating over each .dta file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".dta"):

            filepath = os.path.join(directory, filename)
            data = pd.read_stata(filepath, convert_categoricals=False)
            distinct_columns.update(data.columns)

    # lowerize and sort the columns name
    distinct_columns = [col_name.lower() for col_name in distinct_columns]
    distinct_columns = sorted(distinct_columns)

    # Saving the distinct column names to a file
    with open(f"pages/ChereDoc/column_names/column_names_wave{wave}.txt", "w") as file:
        for column in distinct_columns:
            file.write(column + "\n")

    return distinct_columns


def get_column_names(wave, path_to_txt="pages/ChereDoc/column_names/"):

    column_names = []
    with open(f"{path_to_txt}column_names_wave{str(wave)}.txt", "r") as file:
        for line in file:
            column_names.append(line.strip())

    return column_names


for wave in range(1, 9):
    directory = f"static/data/sharew{wave}_rel9-0-0_ALL_datasets_stata/"
    column_names = save_column_names(directory, wave)
    print(f"Wave {wave} has {len(column_names)} columns\n")
