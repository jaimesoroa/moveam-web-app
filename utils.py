# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import streamlit as st

class Utils:

    def check_config():
        '''Returns a message to user for missing configuration
        
        Returns:
            string: Error info
        '''

        if st.session_state['AUTHENTICATION_MODE'] == '':
            return 'Please specify one of the two authentication modes'
        if st.session_state['AUTHENTICATION_MODE'].lower() == 'serviceprincipal' and st.session_state['TENANT_ID'] == '':
            return 'Tenant ID is not provided'
        elif st.session_state['REPORT_ID'] == '':
            return 'Report ID is not provided'
        elif st.session_state['WORKSPACE_ID'] == '':
            return 'Workspace ID is not provided'
        elif st.session_state['CLIENT_ID'] == '':
            return 'Client ID is not provided'
        elif st.session_state['AUTHENTICATION_MODE'].lower() == 'masteruser':
            if st.session_state['POWER_BI_USER'] == '':
                return 'Master account username is not provided'
            elif st.session_state['POWER_BI_PASS'] == '':
                return 'Master account password is not provided'
        elif st.session_state['AUTHENTICATION_MODE'].lower() == 'serviceprincipal':
            if st.session_state['CLIENT_SECRET'] == '':
                return 'Client secret is not provided'
        elif st.session_state['SCOPE_BASE'] == '':
            return 'Scope base is not provided'
        elif st.session_state['AUTHORITY_URL'] == '':
            return 'Authority URL is not provided'
        
        return None