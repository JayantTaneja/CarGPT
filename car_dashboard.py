import streamlit as st
from utils.dashboard_utils import *

st.set_page_config(
    page_title="Car Dashboard",
    layout="wide"
)


if 'setup' not in st.session_state.keys():

    st.session_state['setup'] = True
    
    setup()
    show_startup()
    start_server()