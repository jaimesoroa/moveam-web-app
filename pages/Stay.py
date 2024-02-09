import streamlit as st
import pandas as pd
import numpy as np
from st_on_hover_tabs import on_hover_tabs
import os
from st_pages import Page, Section, show_pages, add_page_title
import altair as alt
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
    
    stay_authorized_users = ['jsoroa', 'fperez', 'jfuster', 'aheras']
    if st.session_state['username'] in stay_authorized_users:
        st.write(f'Bienvenido a la página de propiedades de Stay')#, *{st.session_state["name"]}*')

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

        WORKSPACE_ID = st.session_state['power_bi_moveam_wokspace_id']
        # REPORT_ID = st.session_state['powerbi_stay_id']
        REPORT_IDS = [st.session_state['powerbi_stay_id'], st.session_state['powerbi_tarragona_id'], st.session_state['powerbi_cordoba_id']]
        
        # ===============================================================================================================
        # Functions
        
        # @st.cache_data
        # def create_apartment_list_tarragona():
        #     apartment_list = []
        #     for i in range(9):
        #         apartment_list.extend(range(101+i*100, 117+i*100))
        #     return apartment_list

        # apartment_list_tarragona = create_apartment_list_tarragona()
        
        # @st.cache_data
        # def monthly_consumption_flat_tarragona(df, piso):
        #     df_flat_month = pd.DataFrame(df[df['Piso'] == piso].groupby(by= ['Month'])['kWh_diff'].sum()).reset_index()
        #     return df_flat_month
        
        # @st.cache_resource
        def plot_power_bi_stay():
            # return st.markdown(f'<iframe title= {POWER_BI_TARRAGONA_TITLE} width="1140" height="541.25" src={POWER_BI_TARRAGONA_SRC} frameborder="0" allowFullScreen="true"></iframe>', unsafe_allow_html=True)
            # embed_info = PbiEmbedService().get_embed_params_for_single_report(WORKSPACE_ID, REPORT_ID)
            embed_info = PbiEmbedService().get_embed_params_for_multiple_reports(WORKSPACE_ID, REPORT_IDS)
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
                                        width: 1300, // Set the desired width. If too small, the report page gets cut
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
                tabs = on_hover_tabs(tabName=['Centralizado'], 
                                     iconName=['📈'],
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
        
        if tabs == 'Centralizado':
            c1, c2,  = st.columns([15, 1.5], gap='medium')
            with c1:
                st.title("Consumos centralizados de Stay")
            with c2:
                if st.session_state['logo'] == "moveam":
                    st.image('images/Moveam_Transp.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
                else:
                    st.image('images/logo-stay-blanco-trans_2.png', caption=None, use_column_width=True, clamp=False, channels="RGB", output_format="auto")
            st.markdown("""---""")
            
            

            tab_cons_1, tab_cons_2 = st.tabs(["Dashboard", "General"])

            with tab_cons_1:
                st.markdown("Integración de Dashboard")
                # Plot deactivated until issue with Token solved
                plot_power_bi_stay()
                st.markdown("""---""")
                
            with tab_cons_2:
                st.markdown('En construcción')

            
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
                tabs = on_hover_tabs(tabName=['Home'], 
                                     iconName=['🏠'],
                                     default_choice= 0,
                                     styles= {'navtab': {'background-color':'#c4ede3',
                                                          'color': '#818181',
                                                          'font-size': '15px',
                                                          'transition': '.3s',
                                                          'white-space': 'nowrap',
                                                          'text-transform': 'None'}},
                                     key="0")
