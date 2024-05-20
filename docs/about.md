
# SHARE
***

> *"The Survey of Health, Ageing and Retirement in Europe (SHARE) is a research infrastructure for studying the effects of health, social, economic and environmental policies over the life-course of European citizens and beyond"* [from SHARE's website](https://share-eric.eu/)

Key numbers:

- 9 waves
- 24 years
- 530000 interviews
- 28 countries
- almost 4000 publications

# autoSHARE
***

autoSHARE is currently developed by [Joseph Barbier](https://www.barbierjoseph.com/) and [Thomas Salanova](https://www.linkedin.com/in/thomas-salanova/), two research enthusiasts who want to improve and facilitate social science research.

## Motivation
***

We (autoSHARE's developers) believe that [SHARE](https://share-eric.eu/) contains a **wealth of information** that can be used to answer a wide range of research/policy/clinical questions. However, we also believe that the complexity of SHARE data can be a barrier for many potential users.

This is why we developed **autoSHARE**, a web application that simplifies data analysis in SHARE. We also believe that technical problems should not restrein the use of SHARE data, and that technology can make science more efficient, transparent and reproducible.

## What autoSHARE does
***

autoSHARE provides a user-friendly interface to manipulate, clean and analyze SHARE data. It is designed to make reproducible research easier, and to facilitate the use of SHARE data for a wide range of users.

This project is a PoC (Proof of Concept) and is still in development. Our goal is to create a tool able to:

- Load SHARE data, for one or multiple waves ✅
- Clean and harmonize SHARE data ✅
- Manage missing values with different methods ✅
- Manage outliers with different methods ✅
- Visualize data with interactive widgets ❌
- Perform statistical modeling ❌
- Save, export and share results easily ❌

## How autoSHARE works
***

autoSHARE uses the `streamlit` library for the user interface, and other Python packages that you can find [here](https://github.com/JosephBARBIERDARNAL/autoSHARE/blob/main/requirements.txt).

When interacting with the app, the user can

- load data by specifying the wave and the variables of interest

- manage missing values and outliers

- visualize data with interactive widgets

- perform statistical modeling (supervised and unsupervised)

- save, export and share results easily

The aim of this app is to faster common pre-processing tasks related SHARE data, and to make the data more accessible to a wider audience. At any step of the process, the user can download the data, and gain lots of time in the data cleaning process.

A more in-depth explanation of the code can be found [on the source directory](source/index.md).

## Code
***

The entire source code is available on [GitHub](https://github.com/JosephBARBIERDARNAL/autoSHARE). Contributions, bug reports, feature requests and feedback are welcome.

Even small contributions or feedback help us a lot!
