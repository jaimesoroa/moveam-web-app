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
from streamlit_extras.switch_page_button import switch_page

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

# Import the YAML file with the users information
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

st.session_state['authenticator'] = authenticator

# Render the login widget by providing a name for the form and its location (i.e., sidebar or main)
name, authentication_status, username = authenticator.login('Login', 'main')


# use the return values to read the name, authentication_status, and username of the authenticated user.
# ppt-in can be done for a logout button and add it as follows
if authentication_status:
    st.write(f'Welcome to Moveam, *{name}*')
    
    # It's possible to swithc automatically to another page:
    # switch_page("Home")
    
    # Logout button
    authenticator.logout('Logout', 'main')
    
    # Pages to be shown when looged in
    # Specify what pages should be shown in the sidebar, and what their titles and icons should be
    show_pages(
        [
            Page("moveam_app/Home.py", "Home", ":computer:"),
            Page("moveam_app/pages/Tarragona.py", "Tarragona", "🏠"),
            Page("moveam_app/pages/Almeria.py", "Almería", "🏠"),
            Page("moveam_app/pages/Torrejon.py", "Torrejón", "🏠")
        ]
        )
    
    # ===============================================================================================================
    # Beginning of page

    st.markdown('<style>' + open('moveam_app/style.css').read() + '</style>', unsafe_allow_html=True)

    # Add Moveam logo in sidebar
    # st.sidebar.image('moveam_app/images/Moveam_Transp.png')
    # st.sidebar.write("___")

    with st.sidebar:
            tabs = on_hover_tabs(tabName=['Propiedades', 'Sobre Moveam'], 
                                 iconName=['🏠', 'information'],
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

        tab_prop_1, tab_prop_2, tab_prop_3 = st.tabs(["Tarragona", "Almería", "Torrejón"])

        with tab_prop_1:
            st.markdown("Información de la propiedad, con algo gráfico que lo haga atractivo")
            tarragona_analitica = st.button('Ir a la página de analítica de la propiedad', key = 'tarragona_analitica')
            if tarragona_analitica:
                switch_page('Tarragona')
            st.markdown("Se pueden integrar mapas por ejemplo")
            map_data = pd.DataFrame(
            np.random.randn(150, 2) / [50, 50] + [41.12, 1.24],
            columns=['lat', 'lon'])

            st.map(map_data)
            st.markdown("""---""")

        with tab_prop_2:
            st.markdown("Información")
            almeria_analitica = st.button('Ir a la página de analítica de la propiedad', key = 'almeria_analitica')
            if almeria_analitica:
                switch_page('Almería')

        with tab_prop_3:
            st.markdown("Información")
            torrejon_analitica = st.button('Ir a la página de analítica de la propiedad', key = 'torrejon_analitica')
            if torrejon_analitica:
                switch_page('Torrejón')
    
    # ===============================================================================================================
    # Tab Otros

    elif tabs == 'Sobre Moveam':
        c1, c2,  = st.columns([15, 1.5], gap='medium')
        with c1:
            st.title("Sobre Moveam")
            st.write("Conócenos en [link](https://moveam.com/)")
        with c2:
            st.image('moveam_app/images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
        
    
# Rest of instructions below to be copied at the end

# elif authentication_status == False:
#     st.error('Username/password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')

###########################################################
# Another way of doing the same:

# if st.session_state["authentication_status"]:
#     authenticator.logout('Logout', 'main')
#     st.write(f'Welcome *{st.session_state["name"]}*')
#     st.title('Some content')
# elif st.session_state["authentication_status"] == False:
#     st.error('Username/password is incorrect')
# elif st.session_state["authentication_status"] == None:
#     st.warning('Please enter your username and password')
###########################################################

elif authentication_status == False:
    st.error('Username/password is incorrect')
    
    # Pages to be shown when not logged in
    show_pages(
        [
            Page("moveam_app/Home.py", "Login", ":computer:")
        ]
        )
elif authentication_status == None:
    st.warning('Please enter your username and password')
    
    # Pages to be shown when not logged in
    show_pages(
        [
            Page("moveam_app/Home.py", "Login", ":computer:")
        ]
        )