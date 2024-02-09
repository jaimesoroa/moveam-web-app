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
# import streamlit_authenticator as stauth
# import yaml
# from yaml.loader import SafeLoader
from st_pages import Page, Section, show_pages, add_page_title
from services.pbiembedservice import PbiEmbedService
import json

# ===============================================================================================================
# Page config
         
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
    
    torrejon_authorized_users = ['jsoroa', 'fperez', 'jfuster', 'aheras']
    if st.session_state['username'] in torrejon_authorized_users:
        st.write(f'Bienvenido a la página de detalle de la propiedad de Córdoba')#, *{st.session_state["name"]}*')

        show_pages(
        [
            Page("Home.py", "Home", ":computer:"),
            Page("pages/Stay.py", "Stay", "🏡"),
            Page("pages/Tarragona.py", "Tarragona", "🏡"),
            Page("pages/Valencia.py", "Valencia", "🏢"),
            Page("pages/Torrejon.py", "Torrejón", "🏙️"),
            Page("pages/Cordoba.py", "Córdoba", "🏫"),
            Page("pages/Invitado.py", "Invitado", "🏘️")
        ]
        )
        
        # ===============================================================================================================
        # System variables

        # To be used if necessary for another Power BI dashboard
        # load_dotenv()

        # dirname = os.path.dirname(__file__)

        WORKSPACE_ID = st.session_state['power_bi_moveam_wokspace_id']
        REPORT_ID = st.session_state['powerbi_cordoba_id']
        
        # ===============================================================================================================
        # Functions
        
        # @st.cache_resource
        def plot_power_bi_cordoba():
            # return st.markdown(f'<iframe title= {POWER_BI_TARRAGONA_TITLE} width="1140" height="541.25" src={POWER_BI_TARRAGONA_SRC} frameborder="0" allowFullScreen="true"></iframe>', unsafe_allow_html=True)
            embed_info = PbiEmbedService().get_embed_params_for_single_report(WORKSPACE_ID, REPORT_ID)
            api_response_json = json.dumps(embed_info)
            
            html_code = f'''
                <!DOCTYPE html>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/powerbi-client/2.15.1/powerbi.min.js" integrity="sha512-OWIl8Xrlo8yQjWN5LcMz5SIgNnzcJqeelChqPMIeQGnEFJ4m1fWWn668AEXBrKlsuVbvDebTUJGLRCtRCCiFkg==" crossorigin="anonymous"></script>
                <div id="reportContainer">
                    <iframe width="100%" height=750" src="https://app.powerbi.com/reportEmbed?reportId={REPORT_ID}&groupId={WORKSPACE_ID}" frameborder="0" allowFullScreen="true"></iframe>
                </div>
                <style>
                    #reportContainer {{
                        height: 100vh;
                        width: 100%;
                    }}
                </style>
                <script type="text/javascript">
                    window.onload = function() {{
                        // Parse the JSON data received from the API
                        var apiResponse = JSON.parse({api_response_json});
                        // Extract token and other properties from the parsed data
                        var accessToken = apiResponse.accessToken;
                        var expiration = apiResponse.tokenExpiry;
                        var models = window["powerbi-client"].models;
                        var config = {{
                            type: 'report',
                            tokenType: models.TokenType.Embed,
                            accessToken: accessToken,
                            embedUrl: 'https://app.powerbi.com/reportEmbed?reportId={REPORT_ID}&groupId={WORKSPACE_ID}',
                            settings: {{
                                filterPaneEnabled: true,
                                navContentPaneEnabled: true,
                                panes: {{
                                    filters: {{
                                        expanded: true,
                                        visible: true
                                    }}
                                }},
                                layoutType: models.LayoutType.Custom, // Ensure this property is set to Custom
                                customLayout: {{
                                    displayOption: models.DisplayOption.FitToPage,
                                    pageSize: {{
                                        // These dimensions define the size of the report page.
                                        type: models.PageSizeType.Custom,
                                        // Higher width, smaller page
                                        width: 1300, // Set the desired width
                                        // Height doesn't change the page size, but small height covers the bottom.
                                        height: 720 // Set the desired height
                                    }}
                                }}
                            }}
                        }};
                        var reportContainer = document.getElementById('reportContainer');
                        var report = powerbi.embed(reportContainer, config);
                    }};
                </script>
            '''
            # Display embedded report. These dimensions define the streamlit window.
            st.components.v1.html(html_code, height= 700, width= 1200, scrolling= True)
            st.markdown("""---""")

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
                st.title("Consumos de Córdoba")
            with c2:
                if st.session_state['logo'] == "moveam":
                    st.image('images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
                else:
                    st.image('images/logo-stay-blanco-trans_2.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
            st.markdown("""---""")

            tab_cons_1, tab_cons_2, tab_cons_3 = st.tabs(["Dashboard", "General", "Detalle"])

            with tab_cons_1:
                st.markdown("Integración de Dashboard")
                plot_power_bi_cordoba()
                st.markdown("""---""")
            
            with tab_cons_2:
                st.markdown('En construcción')
                st.markdown("Consumos generales de la propiedad")
                # plot_power_bi_torrejon()
                st.markdown("""---""")

            with tab_cons_3:
                st.markdown('En construcción')
                selected_apt_4 = st.selectbox('Seleccionar la vivienda cuyo consumo desea consultar',
            (101, 102, 103))
                if selected_apt_4 == 101:
                    st.markdown("Aquí pondríamos el detall del consumo del 101")
                if selected_apt_4 == 102:
                    st.markdown("Aquí pondríamos el detall del consumo del 102")
                if selected_apt_4 == 103:
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
            Page("pages/Stay.py", "Stay", "🏡"),
            Page("pages/Tarragona.py", "Tarragona", "🏠"),
            Page("pages/Valencia.py", "Valencia", "🏠"),
            Page("pages/Torrejon.py", "Torrejón", "🏠"),
            Page("pages/Cordoba.py", "Córdoba", "🏫"),
            Page("pages/Invitado.py", "Invitado", "🏘️")
        ]
        )
        st.write('No está autorizado a ver esta propiedad')
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
