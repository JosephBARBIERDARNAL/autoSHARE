# autoSHARE
***

autoSHARE is a web application that allows researchers to **easily access and perform** data cleaning/analysis on the [SHARE](https://share-eric.eu/) data. [Learn more](about.md)

The application is built using Python 3.10.13 and the [Streamlit](https://streamlit.io/) library (full requirements can be found in the `root/requirements.txt` file).

Entire source code can be found on the [GitHub repository](https://github.com/JosephBARBIERDARNAL/autoSHARE).

You can learn how to install the app on the [installation guide](installation-guide.md).



# Technical documentation
***

## Overview

The main file app is at the root of the project and is named `autoSHARE.py`. It relies on various modules that are located in the `src/` directory.

Currently, the project is organized as follows:

- [Module on missing values](source/missing_values.md)
- [Module on outliers](source/outliers.md)

