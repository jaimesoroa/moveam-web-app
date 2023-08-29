import streamlit as st
import pandas as pd
import numpy as np
from st_on_hover_tabs import on_hover_tabs
from datetime import date
import requests
import time as t
import os
import dotenv
from dotenv import load_dotenv

load_dotenv()

dirname = os.path.dirname(__file__)

POWER_BI_TITLE_1 = os.environ.get("POWER_BI_TITLE_1")
POWER_BI_SRC_1 = os.environ.get("POWER_BI_SRC_1")


# ===============================================================================================================
# Page config            
st.set_page_config(
    page_title="Moveam",
    page_icon='moveam_app/images/Moveam_Transp.png',
    layout="wide",
    initial_sidebar_state="auto",
)

if "params" not in st.session_state:
    st.session_state['params'] = dict()
    
st.markdown('<style>' + open('moveam_app/style.css').read() + '</style>', unsafe_allow_html=True)

st.sidebar.image('moveam_app/images/Moveam_Transp.png')
st.sidebar.write("___")

with st.sidebar:
        tabs = on_hover_tabs(tabName=['Propiedades', 'Otros'], 
                             iconName=['🏠', '🗝️'],
                             default_choice= 0,
                             styles= {'navtab': {'background-color':'#c4ede3',
                                                  'color': '#818181',
                                                  'font-size': '15px',
                                                  'transition': '.3s',
                                                  'white-space': 'nowrap',
                                                  'text-transform': 'None'}},
                             key="0")

#############################################################################################
# Options for the hover tabs style        

# styles = {'navtab': {'background-color':'#111',
#                                                   'color': '#818181',
#                                                   'font-size': '18px',
#                                                   'transition': '.3s',
#                                                   'white-space': 'nowrap',
#                                                   'text-transform': 'uppercase'},
#                                        'tabOptionsStyle': {':hover :hover': {'color': 'red',
#                                                                       'cursor': 'pointer'}},
#                                        'iconStyle':{'position':'fixed',
#                                                     'left':'7.5px',
#                                                     'text-align': 'left'},
#                                        'tabStyle' : {'list-style-type': 'none',
#                                                      'margin-bottom': '30px',
#                                                      'padding-left': '30px'}},
#############################################################################################

# ===============================================================================================================
# Tab Propiedades
if tabs =='Propiedades':
    
    c1, c2,  = st.columns([15, 1.5], gap='medium')
    with c1:
        st.title("Propiedades")
    with c2:
        st.image('moveam_app/images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
        
    st.markdown("""---""")
    
    tab_prop_1, tab_prop_2, tab_prop_3 = st.tabs(["Tarragona", "Prop_2", "Prop_3"])
    
    with tab_prop_1:
        st.markdown("Información de la propiedad, con algo gráfico que lo haga atractivo")
        st.markdown("Se pueden integrar mapas por ejemplo")
        map_data = pd.DataFrame(
        np.random.randn(150, 2) / [50, 50] + [41.12, 1.24],
        columns=['lat', 'lon'])

        st.map(map_data)
        st.markdown("""---""")
        
    with tab_prop_2:
        st.markdown("Información")
    
    with tab_prop_3:
        st.markdown("Información")
 
# ===============================================================================================================
# Tab Otros

elif tabs == 'Otros':
    c1, c2,  = st.columns([15, 1.5], gap='medium')
    with c1:
        st.title("Otros")
    with c2:
        st.image('moveam_app/images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
    st.markdown("""---""")
    
