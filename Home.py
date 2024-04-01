import streamlit as st
import pandas as pd
import numpy as np
from st_on_hover_tabs import on_hover_tabs
# from datetime import date
# import requests
# import time as t
import os
# import dotenv
# from dotenv import load_dotenv
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from st_pages import Page, Section, show_pages, add_page_title
from streamlit_extras.switch_page_button import switch_page
# import subprocess
import sys
# import msal
# import time
# import threading
# from botocore.exceptions import ClientError
import altair as alt
import boto3
from botocore.exceptions import ClientError
# from azure.identity import DefaultAzureCredential
# from azure.identity import ClientSecretCredential
# import json
from services.pbiembedservice import PbiEmbedService


# ===============================================================================================================
# Page config

# st.session_state['logo'] = "stay"
st.session_state['logo_cabecera'] = "moveam"

if st.session_state['logo_cabecera'] == "moveam":
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
# it's possible to add menu items (upper right hand menu) inside set_page_config

#   menu_items={
#           'Get Help': 'https://www.extremelycoolapp.com/help',
#           'Report a bug': "https://www.extremelycoolapp.com/bug",
#           'About': "# This is a header. This is an *extremely* cool app!"
#   }
#########################################################################

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
# name, authentication_status, username = authenticator.login('Login', 'main')
name, authentication_status, username = authenticator.login('main')

st.session_state['authentication_status'] = authentication_status
st.session_state['username'] = username

# To generate hashed passwords
# hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

# Define logo based on user
moveam_users = ['jsoroa', 'fperez', 'jfuster', 'invitado']
st.session_state['moveam_users'] = moveam_users
stay_users = ['aheras']
st.session_state['stay_users'] = stay_users

if st.session_state['username'] in moveam_users:
    st.session_state['logo'] = "moveam"
else:
    st.session_state['logo'] = "stay"


if "params" not in st.session_state:
    st.session_state['params'] = dict()


# ===============================================================================================================
# Path and system variables

# Get the parent directory
parent_dir = os.path.dirname(os.path.realpath(__file__))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

# Other path functions
# sys.path.append('../')
# sys.path.insert(0, '../..')

# ===============================================================================================================
# AWS secrets

# PowerBI Dashboards
@st.cache_data
def get_secret_powerbi():

    secret_name = "PowerBI"
    region_name = "eu-west-3"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    
    return eval(secret)

powerbi_secrets = get_secret_powerbi()

st.session_state['powerbi_tarragona_title'] = powerbi_secrets['powerbi_tarragona_title']
st.session_state['powerbi_tarragona_source'] = powerbi_secrets['powerbi_tarragona_source']
st.session_state['powerbi_torrejon_title'] = powerbi_secrets['powerbi_torrejon_title']
st.session_state['powerbi_torrejon_source'] = powerbi_secrets['powerbi_torrejon_source']
st.session_state['powerbi_cordoba_title'] = powerbi_secrets['powerbi_cordoba_title']
st.session_state['powerbi_cordoba_source'] = powerbi_secrets['powerbi_cordoba_source']
st.session_state['power_bi_moveam_wokspace_id'] = powerbi_secrets['power_bi_moveam_wokspace_id']
st.session_state['Moveam_app_microsoft_object_id'] = powerbi_secrets['Moveam_app_microsoft_object_id']
st.session_state['CLIENT_SECRET'] = powerbi_secrets['Moveam_app_microsoft_secret']
st.session_state['Moveam_app_microsoft_secret_id'] = powerbi_secrets['Moveam_app_microsoft_secret_id']
st.session_state['CLIENT_ID'] = powerbi_secrets['Moveam_app_microsoft_app_id']
st.session_state['TENANT_ID'] = powerbi_secrets['Moveam_app_microsoft_tenant_id']
st.session_state['powerbi_tarragona_id'] = powerbi_secrets['powerbi_tarragona_id']
st.session_state['powerbi_torrejon_id'] = powerbi_secrets['powerbi_torrejon_id']
st.session_state['powerbi_cordoba_id'] = powerbi_secrets['powerbi_cordoba_id']
st.session_state['powerbi_valdemoro_title'] = powerbi_secrets['powerbi_valdemoro_title']
st.session_state['powerbi_valdemoro_source'] = powerbi_secrets['powerbi_valdemoro_source']
st.session_state['powerbi_valdemoro_id'] = powerbi_secrets['powerbi_valdemoro_id']
st.session_state['powerbi_stay_title'] = powerbi_secrets['powerbi_stay_title']
st.session_state['powerbi_stay_source'] = powerbi_secrets['powerbi_stay_source']
st.session_state['powerbi_stay_id'] = powerbi_secrets['powerbi_stay_id']
st.session_state['powerbi_stay_additional_dataset'] = powerbi_secrets['powerbi_stay_additional_dataset']
st.session_state['powerbi_stay_additional_dataset_2'] = powerbi_secrets['powerbi_stay_additional_dataset_2']
st.session_state['powerbi_stay_own_dataset'] = powerbi_secrets['powerbi_stay_own_dataset']
st.session_state['powerbi_almeria_title'] = powerbi_secrets['powerbi_almeria_title']
st.session_state['powerbi_almeria_source'] = powerbi_secrets['powerbi_almeria_source']
st.session_state['powerbi_almeria_id'] = powerbi_secrets['powerbi_almeria_id']


# Load configuration

# Can be set to 'MasterUser' or 'ServicePrincipal'
AUTHENTICATION_MODE = 'ServicePrincipal'
st.session_state['AUTHENTICATION_MODE'] = AUTHENTICATION_MODE
# Scope Base of AAD app. Use the below configuration to use all the permissions provided in the AAD app through Azure portal.
SCOPE_BASE = ['https://analysis.windows.net/powerbi/api/.default']
st.session_state['SCOPE_BASE'] = SCOPE_BASE
# URL used for initiating authorization request
AUTHORITY_URL = 'https://login.microsoftonline.com/organizations'
st.session_state['AUTHORITY_URL'] = AUTHORITY_URL
# Master user email address. Required only for MasterUser authentication mode.
POWER_BI_USER = ''
st.session_state['POWER_BI_USER'] = POWER_BI_USER
# Master user email password. Required only for MasterUser authentication mode.
POWER_BI_PASS = ''
st.session_state['POWER_BI_PASS'] = POWER_BI_PASS


# ===============================================================================================================
# Get CSV downloaded from Database

@st.cache_data(ttl= 3600)
def read_consumption_tarragona():
    data_tarragona = pd.read_csv("data/db_download/kWh_tarragona.csv")
    # Create Month column and change Date_Hour format
    data_tarragona['Month'] = pd.DatetimeIndex(data_tarragona['Date']).month
    data_tarragona['Date'] = pd.to_datetime(data_tarragona['Date'])
    return data_tarragona

# st.session_state['data_tarragona'] = read_consumption_tarragona()

@st.cache_data(ttl= 3600)
def monthly_consumption(df):
    df_month = pd.DataFrame(df.groupby(by= 'Month')['kWh_diff'].sum())
    df_month['Month'] = df_month.index
    return df_month

# st.session_state['data_tarragona_month'] = monthly_consumption(st.session_state['data_tarragona'])

# ===============================================================================================================
# Other functions

# @st.cache_data(ttl= 3600)
def show_pages_all():
    show_pages(
            [
                Page("Home.py", "Home", ":computer:"),
                Page("pages/Stay.py", "Stay", "🏛️"),
                Page("pages/Tarragona.py", "Tarragona", "🏘️"),
                Page("pages/Valencia.py", "Valencia", "🏢"),
                Page("pages/Torrejon.py", "Torrejón", "🏙️"),
                Page("pages/Cordoba.py", "Córdoba", "🏫"),
                Page("pages/Almeria.py", "Almería", "🏤"),
                Page("pages/Invitado.py", "Invitado", "🏡")
            ]
            )
    return None

# @st.cache_data(ttl= 3600)
def show_pages_stay():
    show_pages(
            [
                Page("Home.py", "Home", ":computer:"),
                Page("pages/Stay.py", "Stay", "🏛️"),
                Page("pages/Tarragona.py", "Tarragona", "🏘️"),
                Page("pages/Valencia.py", "Valencia", "🏢"),
                Page("pages/Torrejon.py", "Torrejón", "🏙️"),
                Page("pages/Cordoba.py", "Córdoba", "🏫")
            ]
            )
    return None

def show_pages_home():
    show_pages(
            [
                Page("Home.py", "Home", ":computer:"),
                Page("pages/Invitado.py", "Invitado", "🏡")
            ]
            )
    return None

# @st.cache_data(ttl= 3600)
def tabs_all():
    tab_prop_1, tab_prop_2, tab_prop_3, tab_prop_4, tab_prop_5, tab_prop_6, tab_prop_7 = st.tabs(["Stay", "Tarragona", "Valencia", "Torrejón", "Córdoba", "Almería", "Invitado"])

    with tab_prop_1:
        stay_analitica = st.button('Ir a la página de centralización de propiedades de Stay', key = 'stay_analitica')
        if stay_analitica:
            switch_page('Stay')
    
    with tab_prop_2:
        # st.metric(label="Consumo de energía del último mes", value="18.500 kWh", delta="+2%")
        # st.markdown("Información de la propiedad")
        tarragona_analitica = st.button('Ir a la página de analítica de la propiedad', key = 'tarragona_analitica')
        if tarragona_analitica:
            switch_page('Tarragona')
        # st.markdown("Se pueden integrar mapas por ejemplo")
        # map_data = pd.DataFrame(
        # np.random.randn(150, 2) / [50, 50] + [41.12, 1.24],
        # columns=['lat', 'lon'])
        # st.map(map_data)
        st.markdown("""---""")
        
    with tab_prop_3:
        # st.markdown("Información")
        valencia_analitica = st.button('Ir a la página de analítica de la propiedad', key = 'valencia_analitica')
        if valencia_analitica:
            switch_page('Valencia')
    with tab_prop_4:
        # st.markdown("Información")
        torrejon_analitica = st.button('Ir a la página de analítica de la propiedad', key = 'torrejon_analitica')
        if torrejon_analitica:
            switch_page('Torrejón')
    
    with tab_prop_5:
        # st.markdown("Información")
        cordoba_analitica = st.button('Ir a la página de analítica de la propiedad', key = 'cordoba_analitica')
        if cordoba_analitica:
            switch_page('Córdoba')
            
    with tab_prop_6:
        # st.markdown("Información")
        cordoba_analitica = st.button('Ir a la página de analítica de la propiedad', key = 'almeria_analitica')
        if cordoba_analitica:
            switch_page('Almería')
    
    with tab_prop_7:
        # st.markdown("Información")
        invitado_analitica = st.button('Ir a la página de analítica de la propiedad', key = 'invitado_analitica')
        if invitado_analitica:
            switch_page('Invitado')
            
    return None

# @st.cache_data(ttl= 3600)
def tabs_stay():
    tab_prop_1, tab_prop_2, tab_prop_3, tab_prop_4, tab_prop_5 = st.tabs(["Stay", "Tarragona", "Valencia", "Torrejón", "Córdoba"])

    with tab_prop_1:
        stay_analitica = st.button('Ir a la página de centralización de propiedades de Stay', key = 'stay_analitica')
        if stay_analitica:
            switch_page('Stay')
    
    with tab_prop_2:
        # st.metric(label="Consumo de energía del último mes", value="18.500 kWh", delta="+2%")
        # st.markdown("Información de la propiedad")
        tarragona_analitica = st.button('Ir a la página de analítica de la propiedad', key = 'tarragona_analitica')
        if tarragona_analitica:
            switch_page('Tarragona')
        # st.markdown("Se pueden integrar mapas por ejemplo")
        # map_data = pd.DataFrame(
        # np.random.randn(150, 2) / [50, 50] + [41.12, 1.24],
        # columns=['lat', 'lon'])
        # st.map(map_data)
        st.markdown("""---""")
        
    with tab_prop_3:
        # st.markdown("Información")
        valencia_analitica = st.button('Ir a la página de analítica de la propiedad', key = 'valencia_analitica')
        if valencia_analitica:
            switch_page('Valencia')
    with tab_prop_4:
        # st.markdown("Información")
        torrejon_analitica = st.button('Ir a la página de analítica de la propiedad', key = 'torrejon_analitica')
        if torrejon_analitica:
            switch_page('Torrejón')
    
    with tab_prop_5:
        # st.markdown("Información")
        cordoba_analitica = st.button('Ir a la página de analítica de la propiedad', key = 'cordoba_analitica')
        if cordoba_analitica:
            switch_page('Córdoba')
            
    return None

# ===============================================================================================================
# Authentication privileges

# use the return values to read the name, authentication_status, and username of the authenticated user.
# ppt-in can be done for a logout button and add it as follows
if authentication_status:
    c1, c2, c3 = st.columns([3, 13, 2], gap='medium')
    with c1:
        if st.session_state['logo'] == "moveam":
            st.image('images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
        else:
            st.image('images/logo-stay-blanco-trans_2.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
    with c2:
        st.write('')
        st.write('')
        st.write('')
        # st.write(f'Bienvenido, *{name}*')
    with c3:
        # Logout button
        authenticator.logout('Logout', 'main')
        # Reset password widget
        # if st.button('Reset password'):
        #     st.session_state['Reset_password'] = 'Yes'
        # else:
        #     st.session_state['Reset_password'] = 'No'
    
    # if st.session_state['Reset_password']=='Yes':
    #     try:
    #         if authenticator.reset_password(username, 'Reset password'):
    #             st.success('Password modified successfully')
    #             # st.session_state['Reset_password'] = 'No'
    #     except Exception as e:
    #         st.error(e)
    # else:
    #     st.markdown('')
    
    # It's possible to switch automatically to another page:
    # switch_page("Home")
    
    # Pages to be shown when looged in
    # Specify what pages should be shown in the sidebar, and what their titles and icons should be
    
    if st.session_state['username'] in moveam_users:
        show_pages_all()
    elif st.session_state['username'] in stay_users:
        show_pages_stay()
    else:
        show_pages_home()   
    
    
    # ===============================================================================================================
    # Beginning of page

    st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)
    
    
    # Add Moveam logo in sidebar
    # st.sidebar.image('images/Moveam_Transp.png')
    # st.sidebar.write("___")

    # Add a sction title
    # section_title  = '<p style="font-family:Arial; color:Black; font-size: 12px;">Secciones</p>'
    # st.sidebar.markdown(section_title, unsafe_allow_html=True)

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
            st.write('')

        st.markdown("""---""")
        
        if st.session_state['username'] in moveam_users:
            tabs_all()
        else:
            tabs_stay()
    
    # ===============================================================================================================
    # Tab Otros

    elif tabs == 'Sobre Moveam':
        c1, c2,  = st.columns([15, 1.5], gap='medium')
        with c1:
            st.title("Sobre Moveam")
            st.write("Conócenos en [link](https://moveam.com/)")
        with c2:
            st.write('---')
            #st.image('images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
        
    
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
    st.error('Usuario/contraseña incorrectos')
    
    # Pages to be shown when not logged in
    show_pages(
        [
            Page("Home.py", "Login", ":computer:")
        ]
        )
elif authentication_status == None:
    st.warning('Por favor introduzca su nombre de usuario y contraseña')
    
    # Pages to be shown when not logged in
    show_pages(
        [
            Page("Home.py", "Login", ":computer:")
        ]
        )