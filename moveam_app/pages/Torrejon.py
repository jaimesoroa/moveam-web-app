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
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from st_pages import Page, Section, show_pages, add_page_title

# ===============================================================================================================
# Page config
         
st.set_page_config(
    page_title="Moveam",
    page_icon='moveam_app/images/Moveam_Transp.png',
    layout="wide",
    initial_sidebar_state="auto"
)
#########################################################################
# it's possible to add menu iteams (upper right hand menu) inside set_page_config

#   menu_items={
#           'Get Help': 'https://www.extremelycoolapp.com/help',
#           'Report a bug': "https://www.extremelycoolapp.com/bug",
#           'About': "# This is a header. This is an *extremely* cool app!"
#   }
#########################################################################

if "params" not in st.session_state:
    st.session_state['params'] = dict()

# ===============================================================================================================
# Authentication

if not st.session_state["authentication_status"]:
    st.write('Please login')
    show_pages(
        [
            Page("moveam_app/Home.py", "Login", "🏠")
        ]
        )

else:
    # show_pages(
    #     [
    #         Page("moveam_app/Home.py", "Home", ":computer:"),
    #         Page("moveam_app/pages/Tarragona.py", "Tarragona", "🏠"),
    #         Page("moveam_app/pages/Almeria.py", "Almería", "🏠"),
    #         Page("moveam_app/pages/Torrejon.py", "Torrejón", "🏠")            
    #     ]
    #     )

    # ===============================================================================================================
    # User authorization
    
    almeria_authorized_users = ['jsoroa']
    if st.session_state['username'] in almeria_authorized_users:
        st.write(f'Welcome to Moveam, *{st.session_state["name"]}*')

        show_pages(
        [
            Page("moveam_app/Home.py", "Home", ":computer:"),
            Page("moveam_app/pages/Tarragona.py", "Tarragona", "🏠"),
            Page("moveam_app/pages/Almeria.py", "Almería", "🏠"),
            Page("moveam_app/pages/Torrejon.py", "Torrejón", "🏠")
        ]
        )
        
        # ===============================================================================================================
        # System variables

        # To be used if necessary for another Power BI dashboard
        load_dotenv()

        dirname = os.path.dirname(__file__)

        POWER_BI_TITLE_1 = os.environ.get("POWER_BI_TITLE_1")
        POWER_BI_SRC_1 = os.environ.get("POWER_BI_SRC_1")

        # ===============================================================================================================
        # Beginning of page


        st.markdown('<style>' + open('moveam_app/style.css').read() + '</style>', unsafe_allow_html=True)

        with st.sidebar:
                tabs = on_hover_tabs(tabName=['Consumos', 'Vehículos', 'Zonas comunes', 'Informes'], 
                                     iconName=['📈', '🅿️', '📹', '📋'],
                                     default_choice= 0,
                                     styles= {'navtab': {'background-color':'#c4ede3',
                                                          'color': '#818181',
                                                          'font-size': '15px',
                                                          'transition': '.3s',
                                                          'white-space': 'nowrap',
                                                          'text-transform': 'None'}},
                                     key="0")
                
        # ===============================================================================================================
        # Tab Consumos

        if tabs == 'Consumos':
            c1, c2,  = st.columns([15, 1.5], gap='medium')
            with c1:
                st.title("Consumos")
            with c2:
                st.image('moveam_app/images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
            st.markdown("""---""")

            @st.cache_resource
            def plot_power_bi_1():
                return st.markdown(f'<iframe title= {POWER_BI_TITLE_1} width="1140" height="541.25" src={POWER_BI_SRC_1} frameborder="0" allowFullScreen="true"></iframe>', unsafe_allow_html=True)

            tab_cons_1, tab_cons_2 = st.tabs(["General", "Detalle"])

            with tab_cons_1:
                st.markdown("Integración de Dashboard de Power BI")
                plot_power_bi_1()
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

            st.markdown("Gestión de vehículos, hay que darle una vuelta para mejorar lo que hay en la aplicación")

        # ===============================================================================================================
        # Tab Zonas Comunes

        elif tabs == 'Zonas comunes':
            c1, c2,  = st.columns([15, 1.5], gap='medium')
            with c1:
                st.title("Zonas comunes")
            with c2:
                st.image('moveam_app/images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
            st.markdown("""---""")

            st.markdown("Aquí añadiríamos estadísticas de las zonas comunes")

        # ===============================================================================================================
        # Tab Informes

        elif tabs == 'Informes':
            c1, c2,  = st.columns([15, 1.5], gap='medium')
            with c1:
                st.title("Informes")
            with c2:
                st.image('moveam_app/images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
            st.markdown("""---""")

            st.markdown("Herramientas de generación de informes")

    else:
        st.write('You are not authorized to see this property')
        show_pages(
        [
            Page("moveam_app/Home.py", "Home", ":computer:"),
            Page("moveam_app/pages/Tarragona.py", "Tarragona", "🏠"),
            Page("moveam_app/pages/Almeria.py", "Almería", "🏠"),
            Page("moveam_app/pages/Torrejon.py", "Torrejón", "🏠")
        ]
        )
        
        st.markdown('<style>' + open('moveam_app/style.css').read() + '</style>', unsafe_allow_html=True)
        
        with st.sidebar:
                tabs = on_hover_tabs(tabName=[''], 
                                     iconName=[''],
                                     default_choice= 0,
                                     styles= {'navtab': {'background-color':'#c4ede3',
                                                          'color': '#818181',
                                                          'font-size': '15px',
                                                          'transition': '.3s',
                                                          'white-space': 'nowrap',
                                                          'text-transform': 'None'}},
                                     key="0")
