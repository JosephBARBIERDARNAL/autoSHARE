import pandas as pd
import os
from glob import glob
import pyreadstat


def get_descriptions(path, output_dir):
    data, meta = pyreadstat.read_dta(path)
    names_and_labels = pd.DataFrame(
        {"NomVariable": meta.column_names, "Label": meta.column_labels}
    )
    nom_fichier_csv = os.path.basename(path).replace(".dta", ".csv")
    path_csv = os.path.join(output_dir, nom_fichier_csv)
    # print(path_csv)
    # names_and_labels.to_csv(path_csv, index=False)


input_dirs = [
    f"static/data/sharew{i}_rel9-0-0_ALL_datasets_stata" for i in range(1, 10)
]
output_dir = "static/columns"
os.makedirs(output_dir, exist_ok=True)

for input_dir in input_dirs:
    fichiers_dta = glob(os.path.join(input_dir, "*.dta"))
    for fichier_dta in fichiers_dta:
        get_descriptions(fichier_dta, output_dir)
