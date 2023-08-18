import streamlit as st
import pandas as pd
import numpy as np
from st_on_hover_tabs import on_hover_tabs
from datetime import date
import requests
import time as t

# ===============================================================================================================
# Page config            
st.set_page_config(
    page_title="Moveam",
    page_icon='⚕️',
    layout="wide",
    initial_sidebar_state="auto",
)

st.markdown('<style>' + open('moveam_app/style.css').read() + '</style>', unsafe_allow_html=True)

with st.sidebar:
        tabs = on_hover_tabs(tabName=['Propiedades', 'Consumos', 'Vehículos'], 
                             iconName=['dashboard', 'money', 'economy'],
                             key="0")

# ===============================================================================================================
# Tab Dashboard