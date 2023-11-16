import streamlit as st
import pandas as pd
import numpy as np
from st_on_hover_tabs import on_hover_tabs
from datetime import date
# import requests
# import time as t
# import os
# import dotenv
from dotenv import load_dotenv
import streamlit_authenticator as stauth
# import yaml
# from yaml.loader import SafeLoader
from st_pages import Page, Section, show_pages, add_page_title

# ===============================================================================================================
# Page config
         
if st.session_state['logo'] == "moveam":
    st.set_page_config(
        page_title="Moveam",
        page_icon='images/Moveam_Transp.png',
        layout="wide",
        initial_sidebar_state="auto"
    )
else:
    st.set_page_config(
        page_title="Moveam",
        page_icon='images/logo-stay-blanco-trans_2.png',
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
            Page("Home.py", "Login", "🏠")
        ]
        )

else:
    
    # ===============================================================================================================
    # User authorization
    
    valencia_authorized_users = ['jsoroa', 'fperez', 'jfuster', 'aheras']
    if st.session_state['username'] in valencia_authorized_users:
        st.write(f'Bienvenido a la página de detalle de la propiedad de Valencia')#, *{st.session_state["name"]}*')

        show_pages(
        [
            Page("Home.py", "Home", ":computer:"),
            Page("pages/Tarragona.py", "Tarragona", "🏡"),
            Page("pages/Valencia.py", "Valencia", "🏢"),
            Page("pages/Torrejon.py", "Torrejón", "🏙️"),
            Page("pages/Cordoba.py", "Córdoba", "🏫")
        ]
        )
        
        # ===============================================================================================================
        # System variables

        # To be used if necessary for another Power BI dashboard
        # load_dotenv()

        # dirname = os.path.dirname(__file__)

        # POWER_BI_TITLE_1 = os.environ.get("POWER_BI_TITLE_1")
        # POWER_BI_SRC_1 = os.environ.get("POWER_BI_SRC_1")

        # ===============================================================================================================
        # Beginning of page


        st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

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
                st.title("Consumos de Valencia")
            with c2:
                if st.session_state['logo'] == "moveam":
                    st.image('images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
                else:
                    st.image('images/logo-stay-blanco-trans_2.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
            st.markdown("""---""")

            # @st.cache_resource
            # def plot_power_bi_valencia():
            #     return st.markdown(f'<iframe title= {POWER_BI_TITLE_1} width="1140" height="541.25" src={POWER_BI_SRC_1} frameborder="0" allowFullScreen="true"></iframe>', unsafe_allow_html=True)

            tab_cons_1, tab_cons_2, tab_cons_3 = st.tabs(["Dashboard", "General", "Detalle"])

            with tab_cons_1:
                st.markdown("Integración de Dashboard de Power BI")
                # plot_power_bi_valencia()
                st.markdown("""---""")
            
            with tab_cons_2:
                st.markdown('En construcción')
                st.markdown("Consumos generales de la propiedad")
                # plot_power_bi_valencia()
                st.markdown("""---""")

            with tab_cons_3:
                st.markdown('En construcción')
                selected_apt_2 = st.selectbox('Seleccionar la vivienda cuyo consumo desea consultar',
            (101, 102, 103))
                if selected_apt_2 == 101:
                    st.markdown("Aquí pondríamos el detall del consumo del 101")
                if selected_apt_2 == 102:
                    st.markdown("Aquí pondríamos el detall del consumo del 102")
                if selected_apt_2 == 103:
                    st.markdown("Aquí pondríamos el detall del consumo del 103")
            
            


        # ===============================================================================================================
        # Tab Vehículos

        elif tabs == 'Vehículos':
            c1, c2,  = st.columns([15, 1.5], gap='medium')
            with c1:
                st.title("Vehículos")
            with c2:
                if st.session_state['logo'] == "moveam":
                    st.image('images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
                else:
                    st.image('images/logo-stay-blanco-trans_2.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
            st.markdown("""---""")

            st.markdown("Gestión de vehículos")

        # ===============================================================================================================
        # Tab Zonas Comunes

        elif tabs == 'Zonas comunes':
            c1, c2,  = st.columns([15, 1.5], gap='medium')
            with c1:
                st.title("Zonas comunes")
            with c2:
                if st.session_state['logo'] == "moveam":
                    st.image('images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
                else:
                    st.image('images/logo-stay-blanco-trans_2.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
            st.markdown("""---""")

            st.markdown("Estadísticas de las zonas comunes")

        # ===============================================================================================================
        # Tab Informes

        elif tabs == 'Informes':
            c1, c2,  = st.columns([15, 1.5], gap='medium')
            with c1:
                st.title("Informes")
            with c2:
                if st.session_state['logo'] == "moveam":
                    st.image('images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
                else:
                    st.image('images/logo-stay-blanco-trans_2.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
            st.markdown("""---""")

            st.markdown("Herramientas de generación de informes")

    else:
        show_pages(
        [
            Page("Home.py", "Home", ":computer:"),
            Page("pages/Tarragona.py", "Tarragona", "🏠"),
            Page("pages/Valencia.py", "Valencia", "🏠"),
            Page("pages/Torrejon.py", "Torrejón", "🏠"),
            Page("pages/Cordoba.py", "Córdoba", "🏫")
        ]
        )
        st.write('You are not authorized to see this property')
        st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)
        
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
