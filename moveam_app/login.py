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
    st.write(f'Welcome *{name}*')
    switch_page("Home")
    
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
elif authentication_status == None:
    st.warning('Please enter your username and password')