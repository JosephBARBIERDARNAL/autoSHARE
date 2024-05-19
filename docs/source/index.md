# Overview
***

The main file app is at the root of the project and is named `autoSHARE.py`. It relies on various modules that are located in the `src/` directory.

Currently, the project is organized as follows:


`root/`

- `autoSHARE.py`: main (streamlit) file. This is the file we run to use the app with the `streamlit run autoSHARE.py` command.

- `requirements.txt`: list of dependencies (Python packages) required to run the app.

- `docs/`: directory containing the documentation of the project (the website you are currently reading).

- `src/`: directory containing the modules used by the main file.

      - `constants.py`: module containing a few constants used throughout the app.

      - `utils.py`: module containing various utility functions.

      - `data/`: directory containing the code for data management.

         - `data.py`: module containing the [DataManager](data.md) class.

         - `missing_values.py`: module containing the [MissingValuesManager](missing_values.md) class.

         - `outliers.py`: module containing the [OutliersManager](outliers.md) class.

      - `ui/`: directory containing the code for the user interface.

         - `ui.py`: module containing various functions to create the app's interface.

         - `helps.py`: module containing the strings used for `help` tooltips from streamlit functions.

      - `viz/`: directory containing the code for data visualization.

         - `plot.py`: module containing the [Plot](plot.md) class.

- `static/`: directory containing data and metadata files used by the app, as well as code that generates the metadata files.
