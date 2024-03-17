import pandas as pd
import streamlit as st



@st.cache_data(show_spinner=False)
def load_data_properties(wave: int):
    """
    Load the properties of the columns for the specified wave.
    """
    columns_properties = pd.read_csv(f'static/columns/wave_{wave}_columns.csv')
    return columns_properties




class datasetManager:

    def __init__(self, data_path: str, wave: int):
        self.data_path = data_path
        self.wave = wave

    def create_dataframe(self, cols: list):
        """
        Load the data from the specified columns.
        Args:
            - cols: the columns to load.
        Returns:
            - df: the dataset.
        """

        columns_properties = load_data_properties(self.wave)
        df = pd.DataFrame()

        # get all files needed
        file_names = []
        for col in cols:
            file_name = columns_properties.loc[columns_properties['column']==col, 'file_name'].values[0]
            if file_name not in file_names:
                file_names.append(file_name)

        # load all datasets
        for file_name in file_names:
            full_path = f'{self.data_path}/sharew{self.wave}_rel8-0-0_ALL_datasets_stata/{file_name}'
            temp = pd.read_stata(
                full_path,
                convert_categoricals=False
            )

            # merge with mergeid
            if len(df)==0:
                df = temp
            else:
                df = df.merge(
                    temp,
                    on='mergeid',
                    how='outer'
                )

        df = df[cols]
        self.df = df
        return df
    
    def display_dataset_properties(self, df):
        """
        Display the properties of the dataset.
        Args:
            - df: the dataset.
        """
        st.write("First rows of the dataset:")
        st.dataframe(df.head(5))
        st.success(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        st.warning(f"Memory usage: {df.memory_usage().sum()/(1024*1024):.2f} MB")
        missing_values = df.isna().sum()/df.shape[0]#*100
        missing_values = missing_values.to_frame('missing_values')
        missing_values['column'] = missing_values.index
        missing_values = missing_values.sort_values(by='missing_values', ascending=False)
        c1, used_col, c3 = st.columns([1, 6, 1])
        with used_col:
            st.data_editor(
                missing_values,
                column_config={
                    "missing_values": st.column_config.ProgressColumn(
                        "% of missing values",
                        min_value=0,
                        max_value=1,
                        width='large'
                    ),
                },
                hide_index=True
            )
    
    def replace_missing_code(self, df: pd.DataFrame) -> pd.DataFrame:
        valuesToReplace = [
            "Don't know",
            "Refusal",
            "Implausible value/suspected wrong",
            "Not codable",
            "Not answered",
            "Not yet coded",
            "Not applicable",
            -9999991,
            -9999992,
        ]
        df = df.replace(valuesToReplace, pd.NA)
        self.df = df
        return df