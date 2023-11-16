# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

# from flask import current_app as app
import msal
import streamlit as st

class AadService:

    def get_access_token():
        '''Generates and returns Access token

        Returns:
            string: Access token
        '''

        response = None
        try:
            if st.session_state['AUTHENTICATION_MODE'].lower() == 'masteruser':

                # Create a public client to authorize the app with the AAD app
                clientapp = msal.PublicClientApplication(st.session_state['CLIENT_ID'], authority=st.session_state['AUTHORITY_URL'])
                accounts = clientapp.get_accounts(username=st.session_state['POWER_BI_USER'])

                if accounts:
                    # Retrieve Access token from user cache if available
                    response = clientapp.acquire_token_silent(st.session_state['SCOPE_BASE'], account=accounts[0])

                if not response:
                    # Make a client call if Access token is not available in cache
                    response = clientapp.acquire_token_by_username_password(st.session_state['POWER_BI_USER'], st.session_state['POWER_BI_PASS'], scopes=st.session_state['SCOPE_BASE'])     

            # Service Principal auth is the recommended by Microsoft to achieve App Owns Data Power BI embedding
            elif st.session_state['AUTHENTICATION_MODE'].lower() == 'serviceprincipal':
                authority = st.session_state['AUTHORITY_URL'].replace('organizations', st.session_state['TENANT_ID'])
                clientapp = msal.ConfidentialClientApplication(st.session_state['CLIENT_ID'], client_credential=st.session_state['CLIENT_SECRET'], authority=authority)

                # Make a client call if Access token is not available in cache
                response = clientapp.acquire_token_for_client(scopes=st.session_state['SCOPE_BASE'])

            try:
                return response['access_token']
            except KeyError:
                raise Exception(response['error_description'])

        except Exception as ex:
            raise Exception('Error retrieving Access token\n' + str(ex))