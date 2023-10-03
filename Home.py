import streamlit as st
import pandas as pd
import numpy as np
from st_on_hover_tabs import on_hover_tabs
# from datetime import date
# import requests
import time as t
import os
# import dotenv
from dotenv import load_dotenv
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
import sqlalchemy as db
import boto3
from botocore.exceptions import ClientError
import altair as alt


# ===============================================================================================================
# Page config
         
st.set_page_config(
    page_title="Moveam",
    page_icon='images/Moveam_Transp.png',
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
# Path and system variables

# Get the parent directory
parent_dir = os.path.dirname(os.path.realpath(__file__))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

# System variables from .3nv instead of from AWS secrets
load_dotenv()

SQL_DB_TARRAGONA_USER = os.environ.get("SQL_DB_TARRAGONA_USER")
SQL_DB_TARRAGONA_PWD = os.environ.get("SQL_DB_TARRAGONA_PWD")
SQL_DB_TARRAGONA_SERVER = os.environ.get("SQL_DB_TARRAGONA_SERVER")
SQL_DB_TARRAGONA_DB = os.environ.get("SQL_DB_TARRAGONA_DB")

# Other path functions
# sys.path.append('../')
# sys.path.insert(0, '../..')



# ===============================================================================================================
# AWS secrets
# Temporary commented until I manage to get it work in an instance

# @st.cache_resource
# def get_secret_tarragona_db():

#     secret_name = "db_tarragona_historico_Jaime"
#     region_name = "eu-west-3"

#     # Create a Secrets Manager client
#     session = boto3.session.Session()
#     client = session.client(
#         service_name='secretsmanager',
#         region_name=region_name
#     )

#     try:
#         get_secret_value_response = client.get_secret_value(
#             SecretId=secret_name
#         )
#     except ClientError as e:
#         # For a list of exceptions thrown, see
#         # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
#         raise e

#     # Decrypts secret using the associated KMS key.
#     secret = get_secret_value_response['SecretString']

#     return eval(secret)

# tarragona_secret_jaime = get_secret_tarragona_db()

# SQL_DB_TARRAGONA_USER = tarragona_secret_jaime['username']
# SQL_DB_TARRAGONA_PWD = tarragona_secret_jaime['password']
# SQL_DB_TARRAGONA_SERVER = tarragona_secret_jaime['host']
# SQL_DB_TARRAGONA_DB = tarragona_secret_jaime['dbname']


# ===============================================================================================================
# Database connections

# Connect to database
# @st.cache_resource
# def database_connection(SQL_DB_TARRAGONA_USER, SQL_DB_TARRAGONA_PWD, SQL_DB_TARRAGONA_SERVER, SQL_DB_TARRAGONA_DB):
#     url_db_tarragona = db.URL.create(
#         "mysql+mysqldb",
#         username = SQL_DB_TARRAGONA_USER,
#         password = SQL_DB_TARRAGONA_PWD,
#         host = SQL_DB_TARRAGONA_SERVER,
#         database = SQL_DB_TARRAGONA_DB,
#     )

#     tarragona_db_engine = db.create_engine(url_db_tarragona)

#     with tarragona_db_engine.connect() as conn, conn.begin():
#         data_tarragona = pd.read_sql_table("kWh", conn)
    
#     return data_tarragona

# data_tarragona = database_connection(SQL_DB_TARRAGONA_USER, SQL_DB_TARRAGONA_PWD, SQL_DB_TARRAGONA_SERVER, SQL_DB_TARRAGONA_DB)

# st.session_state['data_tarragona'] = data_tarragona


# Some more examples of database queries


# Make a query
# data_tarragona = pd.read_sql_query('Select * from kWh;', conn)

# selecting specific columns.
# df2 = data.loc[:, ['ProductName', 'Unit', 'Price']]

# read_sql can be used as a wrap function
# THis calls read_sql_query
# df1 = pd.read_sql("Select * FROM Products", conn) 

# This calls read_sql_table
# *requires SQLAlchemy optional dependencies and DB driver
# df2 = pd.read_sql("test_table", "postgres:///test_db")



# Change Date_Hour format
# data_tarragona['Date_Hour'] = pd.to_datetime(data_tarragona['Date_Hour'])

# Create a specific series for the month consumption
# data_tarragona_month = pd.DataFrame(data_tarragona.groupby(by= 'Month')['kWh_diff'].sum())
# data_tarragona_month['Month'] = data_tarragona_month.index

# st.session_state['data_tarragona_month'] = data_tarragona_month

@st.cache_data
def create_apartment_list():
    apartment_list = []
    for i in range(9):
        apartment_list.extend(range(100+i*100, 117+i*100))
    return apartment_list

apartment_list = create_apartment_list()
st.session_state['apartment_list'] = apartment_list

# ===============================================================================================================

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
    c1, c2,  = st.columns([3, 15], gap='medium')
    with c1:
        st.image('images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
    with c2:
        st.write('')
        st.write('')
        st.write('')
        st.write(f'Bienvenido a Moveam, *{name}*')
    
    
    # It's possible to switch automatically to another page:
    # switch_page("Home")
    
    # Logout button
    authenticator.logout('Logout', 'main')
    
    # Pages to be shown when looged in
    # Specify what pages should be shown in the sidebar, and what their titles and icons should be
    show_pages(
        [
            Page("Home.py", "Home", ":computer:"),
            Page("pages/Tarragona.py", "Tarragona", "🏡"),
            Page("pages/Almeria.py", "Almería", "🏢"),
            Page("pages/Torrejon.py", "Torrejón", "🏙️"),
            Page("pages/Cordoba.py", "Córdoba", "🏫")
        ]
        )


    
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

        tab_prop_1, tab_prop_2, tab_prop_3, tab_prop_4 = st.tabs(["Tarragona", "Almería", "Torrejón", "Córdoba"])

        with tab_prop_1:
            st.metric(label="Consumo de energía del último mes", value="18.500 kWh", delta="+2%")
            st.markdown("Información de la propiedad")
            tarragona_analitica = st.button('Ir a la página de analítica de la propiedad', key = 'tarragona_analitica')
            if tarragona_analitica:
                switch_page('Tarragona')
            # st.markdown("Se pueden integrar mapas por ejemplo")
            # map_data = pd.DataFrame(
            # np.random.randn(150, 2) / [50, 50] + [41.12, 1.24],
            # columns=['lat', 'lon'])

            # st.map(map_data)
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
        
        with tab_prop_4:
            st.markdown("Información")
            cordoba_analitica = st.button('Ir a la página de analítica de la propiedad', key = 'cordoba_analitica')
            if cordoba_analitica:
                switch_page('Córdoba')
    
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