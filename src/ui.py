import streamlit as st




def make_space(n: int, sidebar: bool=False):
    """
    Inserts n empty lines in the UI.
    """

    for _ in range(n):
        if sidebar:
            st.sidebar.text('')
        else:
            st.text('')

def horizontal_line():
    """
    Inserts an horizontal line in the UI.
    """

    st.markdown('<hr>', unsafe_allow_html=True)


def load_header(title: str, subtitle: str):
    """
    Loads the header of the app.
    """

    title = f"<h1 style='text-align: center;'>{title}</h1>"
    subtitle = f"<h4 style='text-align: center;'>{subtitle}</h1>"
    st.markdown(title, unsafe_allow_html=True)
    st.markdown(subtitle, unsafe_allow_html=True)


def load_footer():
    """
    Loads the footer of the app.
    """

    make_space(15)
    st.html(
        "<h5 style='text-align: center;'>Developed by <a href='https://www.cieri-analytics.com/' target='_blank'>CIERI Analytics</a></h5>"
    )
    st.html(
        "<h5 style='text-align: center;'>Contribute <a href='https://github.com/JosephBARBIERDARNAL/autoSHARE' target='_blank'>here</a></h5>"
    )


def display_meta(df, key, print_na: bool = True):
    """
    Display the properties of the dataset.
    Args:
        - df: the dataset.
        - key: the key to use for the widgets. See Streamlit documentation.
        - print_na: whether to print the info about missing values.
    """

    with st.expander("Dataset info"):
        make_space(2)

        # display the first rows of the dataset
        st.markdown("Preview of the dataset")
        st.write(df.head())        

        # display statistics about the dataset
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.success(f"{df.shape[0]} rows")
        with col2:
            st.warning(f"Memory usage: {df.memory_usage().sum()/(1024*1024):.2f} MB")
        with col3:
            st.download_button(
            label="Download dataset",
            data=df.to_csv(index=False),
            file_name=f"share_dataset.csv",
            mime="text/csv",
            key=key+"_download"
        )
        make_space(2)
        
        if print_na:

            st.markdown("Missing values")

            # count missing values
            missing_values = df.isna().sum()/df.shape[0]#*100
            missing_values = missing_values.to_frame('missing_values')
            missing_values['column'] = missing_values.index
            missing_values = missing_values.sort_values(by='missing_values', ascending=False)
            
            # display percentage of missing values per column
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
                    hide_index=True,
                    key=key
                )