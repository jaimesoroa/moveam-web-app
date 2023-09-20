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



if not st.session_state["authentication_status"]:
    st.write('Please login')
    show_pages(
        [
            Page("moveam_app/login.py", "Login", "🏠"),
            Page("moveam_app/pages/Home.py", "Home", "🏠")
        ]
        )

else:
    
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.session_state['authenticator'].logout('Logout', 'sidebar')


###########################################################
# Another way of doing the authentication:

# if st.session_state["authentication_status"]:
#     authenticator.logout('Logout', 'main')
#     st.write(f'Welcome *{st.session_state["name"]}*')
#     st.title('Some content')
# elif st.session_state["authentication_status"] == False:
#     st.error('Username/password is incorrect')
# elif st.session_state["authentication_status"] == None:
#     st.warning('Please enter your username and password')
###########################################################


# How to implement user privileges
# Given that the authenticator object returns the username of your logged-in user, you can utilize that 
# to implement user privileges where each user receives a more personalized experience as shown below:

# if authentication_status:
#     authenticator.logout('Logout', 'main')
#     if username == 'jsmith':
#         st.write(f'Welcome *{name}*')
#         st.title('Application 1')
#     elif username == 'rbriggs':
#         st.write(f'Welcome *{name}*')
#         st.title('Application 2')
# elif authentication_status == False:
#     st.error('Username/password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')


# ===============================================================================================================
# Beginning of page

    # Optional -- adds the title and icon to the current page
    # add_page_title("Homeeeeeemmm")

    # Specify what pages should be shown in the sidebar, and what their titles 
    # and icons should be
    
    home_authorized_users = ['jsoroa', 'fperez', 'jfuster']
    if st.session_state['username'] in home_authorized_users:
#         st.write(f'Welcome *{name}*')
#         st.title('Application 1')
#     elif username == 'rbriggs':
#         st.write(f'Welcome *{name}*')
#         st.title('Application 2')

        show_pages(
        [
            Page("moveam_app/login.py", "Login", "🏠"),
            Page("moveam_app/pages/Home.py", "Home", "🏠"),
            Section(name= "Cool section", icon=":pig:"),
            Page("moveam_app/pages/Tarragona.py", "Tarragona", ":books:")
        ]
        )
    else:
        show_pages(
        [
            Page("moveam_app/pages/Home.py", "Home", "🏠"),
            Page("moveam_app/pages/Tarragona.py", "Tarragona", ":books:")
        ]
        )

    # ===============================================================================================================
    # System variables

    load_dotenv()

    dirname = os.path.dirname(__file__)

    POWER_BI_TITLE_1 = os.environ.get("POWER_BI_TITLE_1")
    POWER_BI_SRC_1 = os.environ.get("POWER_BI_SRC_1")

    # ===============================================================================================================
    # Page

    st.markdown('<style>' + open('moveam_app/style.css').read() + '</style>', unsafe_allow_html=True)

    # Add Moveam logo in sidebar
    # st.sidebar.image('moveam_app/images/Moveam_Transp.png')
    # st.sidebar.write("___")

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
        

    
    