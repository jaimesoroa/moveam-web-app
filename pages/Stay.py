import streamlit as st
import pandas as pd
import numpy as np
from st_on_hover_tabs import on_hover_tabs
import os
from st_pages import Page, Section, show_pages, add_page_title
import altair as alt
from services.pbiembedservice import PbiEmbedService
import json
import requests
import json
from models.embedtoken import EmbedToken
from models.embedconfig import EmbedConfig
from models.reportconfig import ReportConfig


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
# Other functions

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
    
    stay_authorized_users = ['jsoroa', 'fperez', 'jfuster', 'aheras', 'crodriguez', 'agarcia']
    if st.session_state['username'] in stay_authorized_users:
        st.write(f'Bienvenido a la página de propiedades de Stay')#, *{st.session_state["name"]}*')
        
        if st.session_state['username'] in st.session_state['moveam_users']:
            show_pages_all()
        else:
            show_pages_stay()

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

        TENANT_ID = st.session_state['TENANT_ID']
        CLIENT_ID = st.session_state['CLIENT_ID']
        CLIENT_SECRET = st.session_state['CLIENT_SECRET']
        WORKSPACE_ID = st.session_state['power_bi_moveam_wokspace_id']
        REPORT_ID = st.session_state['powerbi_stay_id']
        ADDITIONAL_DATASET = st.session_state['powerbi_stay_additional_dataset']
        ADDITIONAL_DATASET_2 = st.session_state['powerbi_stay_additional_dataset_2']
        STAY_OWN_DATASET = st.session_state['powerbi_stay_own_dataset']
        ADDITIONAL_DATASETS = [ADDITIONAL_DATASET, ADDITIONAL_DATASET_2]
        
        # REPORT_IDS = [st.session_state['powerbi_stay_id'], st.session_state['powerbi_tarragona_id'], st.session_state['powerbi_cordoba_id']]
        
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
            embed_info = PbiEmbedService().get_embed_params_for_single_report(WORKSPACE_ID, REPORT_ID)#, ADDITIONAL_DATASET)
            # embed_info = PbiEmbedService().get_embed_params_for_dashboard_of_dashboards(WORKSPACE_ID, REPORT_ID, ADDITIONAL_DATASETS)
            # embed_info = PbiEmbedService().get_embed_params_for_multiple_reports(WORKSPACE_ID, REPORT_IDS)
            api_response_json = json.dumps(embed_info)
            # print(f' API response for plot: {api_response_json}')
            
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
            Page("pages/Stay.py", "Stay", "🏡")
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

'''
# Code from Gemini to request token for dashboard of dashboards.

import requests
import json

def get_embed_token(TENANT_ID, CLIENT_ID, CLIENT_SECRET, REPORT_ID, WORKSPACE_ID, DATASET_1_ID, DATASET_2_ID):
  """
  This function requests an embed token for a Power BI report with access to two datasets.

  Args:
      TENANT_ID (str): Azure Active Directory tenant ID.
      CLIENT_ID (str): Application (client) ID for your application.
      CLIENT_SECRET (str): Client secret for your application.
      REPORT_ID (str): ID of the Power BI report.
      WORKSPACE_ID (str): ID of the workspace containing the report.
      DATASET_1_ID (str): ID of the first dataset used in the report.
      DATASET_2_ID (str): ID of the second dataset used in the report.

  Returns:
      dict: Embed token information or None on error.
  """

  # Resource URL for Power BI API
  resource_url = "https://analysis.windows.net/powerbi/api"

  # Token endpoint URL
  token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/token"

  # Data for requesting access token
  data = {
      "grant_type": "client_credentials",
      "scope": f"https://{TENANT_ID}/{resource_url}/generatetoken",
      "client_id": CLIENT_ID,
      "client_secret": CLIENT_SECRET
  }

  # Get access token
  try:
      response = requests.post(token_url, data=data)
      response.raise_for_status()
      access_token = response.json()["access_token"]
  except requests.exceptions.RequestException as error:
      print(f"Error getting access token: {error}")
      return None

  # Data for requesting embed token
  embed_token_data = {
      "reports": [
          {
              "id": REPORT_ID,
              "datasets": [
                  {
                      "id": DATASET_1_ID,
                      "xmlaPermissions": "ReadOnly"
                  },
                  {
                      "id": DATASET_2_ID,
                      "xmlaPermissions": "ReadOnly"
                  }
              ]
          }
      ]
  }

  # Headers with authorization
  headers = {
      "Authorization": f"Bearer {access_token}",
      "Content-Type": "application/json"
  }

  # URL for generating embed token
  embed_token_url = f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/reports/{REPORT_ID}/GenerateToken"

  # Get embed token
  try:
      response = requests.post(embed_token_url, headers=headers, json=embed_token_data)
      response.raise_for_status()
      return response.json()
  except requests.exceptions.RequestException as error:
      print(f"Error getting embed token: {error}")
      return None

# Example usage (replace with your actual values)
tenant_id = "YOUR_TENANT_ID"
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
report_id = "YOUR_REPORT_ID"
workspace_id = "YOUR_WORKSPACE_ID"
dataset_1_id = "YOUR_DATASET_1_ID"
dataset_2_id = "YOUR_DATASET_2_ID"

embed_token = get_embed_token(tenant_id, client_id, client_secret, report_id, workspace_id, dataset_1_id, dataset_2_id)

if embed_token:
  print(f"Embed token: {embed_token}")
else:
  print("Failed to retrieve embed token")


JavaScript

async function embedReport(accessToken, workspaceId, reportId) {
  // Load the powerbi client library
  const powerbi = window.powerbi;

  // Configuration object for embedding
  const config = {
    type: 'report',
    tokenType: powerbi.models.TokenType.Embed,
    accessToken: accessToken,
    embedUrl: `https://app.powerbi.com/reportEmbed?reportId=${reportId}&groupId=${workspaceId}`,
    permissions: powerbi.models.Permissions.All,
    settings: {
      filterPaneEnabled: true,
      navContentPaneEnabled: true
    }
  };

  // Get the embed container element
  const embedContainer = document.getElementById('embedContainer');

  try {
    // Embed the report
    const report = await powerbi.embed(embedContainer, config);
    console.log("Report embedded successfully!");
  } catch (error) {
    console.error("Error embedding report:", error);
  }
}

// Example usage (replace with your token retrieved from Python)
const embedToken = "YOUR_EMBED_TOKEN";
const workspaceId = "YOUR_WORKSPACE_ID";
const reportId = "YOUR_REPORT_ID";

embedReport(embedToken, workspaceId, reportId);



HTML
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Embed Power BI Report</title>
  <script src="https://cdn.powerbi.com/powerbi-client.js"></script>
</head>
<body>
  <h1>Power BI Report</h1>
  <div id="embedContainer"></div>

  <script>
    // Call the embedReport function from your JavaScript file
    embedReport('YOUR_EMBED_TOKEN', 'YOUR_WORKSPACE_ID', 'YOUR_REPORT_ID');
  </script>
</body>
</html>


'''