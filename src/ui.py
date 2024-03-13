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


def loadHeader(title: str, subtitle: str):
    """
    Loads the header of the app.
    """

    title = f"<h1 style='text-align: center;'>{title}</h1>"
    subtitle = f"<h4 style='text-align: center;'>{subtitle}</h1>"
    st.markdown(title, unsafe_allow_html=True)
    st.markdown(subtitle, unsafe_allow_html=True)


def loadFooter():
    """
    Loads the footer of the app.
    """

    make_space(10)
    st.markdown(
        "<h5 style='text-align: center;'>Developed by <a href='https://www.cieri-analytics.com/' target='_blank'>CIERI Analytics</a></h5>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h5 style='text-align: center;'>Contribute <a href='https://github.com/JosephBARBIERDARNAL/autoSHARE' target='_blank'>here</a></h5>",
        unsafe_allow_html=True
    )