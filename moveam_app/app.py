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
        tabs = on_hover_tabs(tabName=['Propiedades', 'Consumos', 'Vehículos', 'Áreas comunes', 'Informes'], 
                             iconName=['🏠', '📈', '🅿️', '📹', '📋'],
                             default_choice= 1,
                             key="0")

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
        st.markdown("Se pueden integrar mapas fácilmente")
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
# Tab Consumos

elif tabs == 'Consumos':
    c1, c2,  = st.columns([15, 1.5], gap='medium')
    with c1:
        st.title("Consumos")
    with c2:
        st.image('moveam_app/images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
    st.markdown("""---""")
    
    tab_cons_1, tab_cons_2 = st.tabs(["General", "Detalle"])
    
    with tab_cons_1:
        st.markdown("Integración de Dashboard de Power BI")
        st.markdown(f'<iframe title= {POWER_BI_TITLE_1} width="1140" height="541.25" src={POWER_BI_SRC_1} frameborder="0" allowFullScreen="true"></iframe>', unsafe_allow_html=True)
        st.markdown("""---""")
        
    with tab_cons_2:
        
        selected_apt_1 = st.selectbox('Seleccionar la vivienda cuyo consumo desea consultar',
    (101, 102, 103))
        
        if selected_apt_1 == 101:
            st.markdown("Aquí pondríamos el detall del consumo del 101")
        if selected_apt_1 == 102:
            st.markdown("Aquí pondríamos el detall del consumo del 102")
        if selected_apt_1 == 103:
            st.markdown("Aquí pondríamos el detall del consumo del 103")

    
# ===============================================================================================================
# Tab Vehículos

elif tabs == 'Vehículos':
    c1, c2,  = st.columns([15, 1.5], gap='medium')
    with c1:
        st.title("Vehículos")
    with c2:
        st.image('moveam_app/images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
    st.markdown("""---""")
