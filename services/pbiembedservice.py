# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from services.aadservice import AadService
from models.reportconfig import ReportConfig
from models.embedtoken import EmbedToken
from models.embedconfig import EmbedConfig
from models.embedtokenrequestbody import EmbedTokenRequestBody
from utils import Utils
# from flask import current_app as app, abort
import requests
import json
import streamlit as st

class PbiEmbedService:


    def get_azure_ad_token(self, tenant_id, client_id, client_secret):
        url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': client_id,
            'scope': 'https://analysis.windows.net/powerbi/api/.default',
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        return response.json()['access_token']
    
    
    def get_embed_params_for_single_report(self, workspace_id, report_id, additional_dataset_id=None):
        '''Get embed params for a report and a workspace

        Args:
            workspace_id (str): Workspace Id
            report_id (str): Report Id
            additional_dataset_id (str, optional): Dataset Id different than the one bound to the report. Defaults to None.

        Returns:
            EmbedConfig: Embed token and Embed URL
        '''

        report_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}'
        try:
            api_response = requests.get(report_url, headers=self.get_request_header())
            # print(f'Status code of the get_embed_params_for_single_report request: {api_response.status_code}')
            # print(f'{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')

        # if api_response.status_code != 200:
            # abort(api_response.status_code, description=f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')
            # Replace the previous Flask abort command with a new one
            # print(api_response.status_code, f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')

        except Exception as e:
            print(f"An error occurred: {e}")
            print(api_response.status_code, f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')
        
        api_response = json.loads(api_response.text)
        report = ReportConfig(api_response['id'], api_response['name'], api_response['embedUrl'])
        dataset_ids = [api_response['datasetId']]
        # print(f'The dataset_id is: {dataset_ids}')

        # Append additional dataset to the list to achieve dynamic binding later
        if additional_dataset_id is not None:
            dataset_ids.extend(additional_dataset_id)
        # print(f'The dataset_ids are: {dataset_ids}')

        embed_token = self.get_embed_token_for_single_report_single_workspace(report_id, dataset_ids, workspace_id)
        # print(embed_token.token)
        embed_config = EmbedConfig(embed_token.tokenId, embed_token.token, embed_token.tokenExpiry, [report.__dict__])
        return json.dumps(embed_config.__dict__)

    def get_embed_params_for_multiple_reports(self, workspace_id, report_ids, additional_dataset_ids=None):
        '''Get embed params for multiple reports for a single workspace

        Args:
            workspace_id (str): Workspace Id
            report_ids (list): Report Ids
            additional_dataset_ids (list, optional): Dataset Ids which are different than the ones bound to the reports. Defaults to None.

        Returns:
            EmbedConfig: Embed token and Embed URLs
        '''

        # Note: This method is an example and is not consumed in this sample app

        dataset_ids = []

        # To store multiple report info
        reports = []

        for report_id in report_ids:
            report_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}'
            try:
                api_response = requests.get(report_url, headers=self.get_request_header())

            # if api_response.status_code != 200:
                # abort(api_response.status_code, description=f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')
                # Replace the previous Flask abort command with a new one
                # print(api_response.status_code, f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')

            except Exception as e:
                print(f"An error occurred: {e}")
                print(api_response.status_code, f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')
        

            api_response = json.loads(api_response.text)
            report_config = ReportConfig(api_response['id'], api_response['name'], api_response['embedUrl'])
            reports.append(report_config.__dict__)
            dataset_ids.append(api_response['datasetId'])

        # Append additional dataset to the list to achieve dynamic binding later
        if additional_dataset_ids is not None:
            dataset_ids.extend(additional_dataset_ids)

        embed_token = self.get_embed_token_for_multiple_reports_single_workspace(report_ids, dataset_ids, workspace_id)
        embed_config = EmbedConfig(embed_token.tokenId, embed_token.token, embed_token.tokenExpiry, reports)
        return json.dumps(embed_config.__dict__)

    def get_embed_params_for_dashboard_of_dashboards(self, workspace_id, report_id, additional_datasets_ids):
        
        azure_ad_token = self.get_azure_ad_token(st.session_state['TENANT_ID'], st.session_state['CLIENT_ID'], st.session_state['CLIENT_SECRET'])

        report_url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}'
        try:
            api_response = requests.get(report_url, headers=self.get_request_header())
            # print(f'Status code of the get_embed_params_for_single_report request: {api_response.status_code}')
            # print(f'{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')

        # if api_response.status_code != 200:
            # abort(api_response.status_code, description=f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')
            # Replace the previous Flask abort command with a new one
            # print(api_response.status_code, f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')

        except Exception as e:
            print(f"An error occurred: {e}")
            print(api_response.status_code, f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')
        
        api_response = json.loads(api_response.text)
        report = ReportConfig(api_response['id'], api_response['name'], api_response['embedUrl'])
        # dataset_ids = [api_response['datasetId']]
        # print(f'The dataset_id is: {dataset_ids}')

        # Append additional dataset to the list to achieve dynamic binding later
        # if additional_dataset_id is not None:
        #     dataset_ids.extend(additional_dataset_id)
        # print(f'The dataset_ids are: {dataset_ids}')

        embed_token = self.get_embed_token_for_dashboard_of_dashboards(azure_ad_token, workspace_id, report_id, additional_datasets_ids)
        # print(embed_token.token)
        embed_config = EmbedConfig(embed_token.tokenId, embed_token.token, embed_token.tokenExpiry, [report.__dict__])
        return json.dumps(embed_config.__dict__)
    
    def get_embed_token_for_single_report_single_workspace(self, report_id, dataset_ids, target_workspace_id=None):
        '''Get Embed token for single report, multiple datasets, and an optional target workspace

        Args:
            report_id (str): Report Id
            dataset_ids (list): Dataset Ids
            target_workspace_id (str, optional): Workspace Id. Defaults to None.

        Returns:
            EmbedToken: Embed token
        '''

        request_body = EmbedTokenRequestBody()

        for dataset_id in dataset_ids:
            request_body.datasets.append({'id': dataset_id})

        request_body.reports.append({'id': report_id})

        if target_workspace_id is not None:
            request_body.targetWorkspaces.append({'id': target_workspace_id})

        # Generate Embed token for multiple workspaces, datasets, and reports. Refer https://aka.ms/MultiResourceEmbedToken
        embed_token_api = 'https://api.powerbi.com/v1.0/myorg/GenerateToken'
        try:
            api_response = requests.post(embed_token_api, data=json.dumps(request_body.__dict__), headers=self.get_request_header())
            # print(f'Status code of the get_embed_token_for_single_report_single_workspace request: {api_response.status_code}')
            # print(f'{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')

        # if api_response.status_code != 200:
        #     print(api_response.status_code, f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')

        except Exception as e:
            print(f"An error occurred: {e}")
            print(api_response.status_code, f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')
        
        api_response = json.loads(api_response.text)
        # print(f'The api response is: {api_response}')
        embed_token = EmbedToken(api_response['tokenId'], api_response['token'], api_response['expiration'])
        return embed_token

    def get_embed_token_for_multiple_reports_single_workspace(self, report_ids, dataset_ids, target_workspace_id=None):
        '''Get Embed token for multiple reports, multiple dataset, and an optional target workspace

        Args:
            report_ids (list): Report Ids
            dataset_ids (list): Dataset Ids
            target_workspace_id (str, optional): Workspace Id. Defaults to None.

        Returns:
            EmbedToken: Embed token
        '''

        # Note: This method is an example and is not consumed in this sample app

        request_body = EmbedTokenRequestBody()

        for dataset_id in dataset_ids:
            request_body.datasets.append({'id': dataset_id})

        for report_id in report_ids:
            request_body.reports.append({'id': report_id})

        if target_workspace_id is not None:
            request_body.targetWorkspaces.append({'id': target_workspace_id})

        # Generate Embed token for multiple workspaces, datasets, and reports. Refer https://aka.ms/MultiResourceEmbedToken
        embed_token_api = 'https://api.powerbi.com/v1.0/myorg/GenerateToken'
        try:
            api_response = requests.post(embed_token_api, data=json.dumps(request_body.__dict__), headers=self.get_request_header())

        # if api_response.status_code != 200:
        #     print(api_response.status_code, description=f'Error while retrieving Embed token\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')
        
        except Exception as e:
            print(f"An error occurred: {e}")
            print(api_response.status_code, f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')
                
        api_response = json.loads(api_response.text)
        # print(api_response)
        embed_token = EmbedToken(api_response['tokenId'], api_response['token'], api_response['expiration'])
        return embed_token

    def get_embed_token_for_multiple_reports_multiple_workspaces(self, report_ids, dataset_ids, target_workspace_ids=None):
        '''Get Embed token for multiple reports, multiple datasets, and optional target workspaces

        Args:
            report_ids (list): Report Ids
            dataset_ids (list): Dataset Ids
            target_workspace_ids (list, optional): Workspace Ids. Defaults to None.

        Returns:
            EmbedToken: Embed token
        '''

        # Note: This method is an example and is not consumed in this sample app

        request_body = EmbedTokenRequestBody()

        for dataset_id in dataset_ids:
            request_body.datasets.append({'id': dataset_id})

        for report_id in report_ids:
            request_body.reports.append({'id': report_id})

        if target_workspace_ids is not None:
            for target_workspace_id in target_workspace_ids:
                request_body.targetWorkspaces.append({'id': target_workspace_id})

        # Generate Embed token for multiple workspaces, datasets, and reports. Refer https://aka.ms/MultiResourceEmbedToken
        embed_token_api = 'https://api.powerbi.com/v1.0/myorg/GenerateToken'
        
        try:
            api_response = requests.post(embed_token_api, data=json.dumps(request_body.__dict__), headers=self.get_request_header())

        # if api_response.status_code != 200:
        #     abort(api_response.status_code, description=f'Error while retrieving Embed token\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')

        except Exception as e:
            print(f"An error occurred: {e}")
            print(api_response.status_code, f'Error while retrieving Embed URL\n{api_response.reason}:\t{api_response.text}\nRequestId:\t{api_response.headers.get("RequestId")}')
        
        api_response = json.loads(api_response.text)
        embed_token = EmbedToken(api_response['tokenId'], api_response['token'], api_response['expiration'])
        return embed_token

    def get_embed_token_for_dashboard_of_dashboards(self, access_token, workspace_id, report_id, dataset_ids):
        
        url = f'https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}/GenerateToken'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        data = {
            'accessLevel': 'View',
            'datasets': [{'id': dataset_id} for dataset_id in dataset_ids]
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors

        api_response = json.loads(response.text)
        # print(f'The api response is: {api_response}')
        embed_token = EmbedToken(api_response['tokenId'], api_response['token'], api_response['expiration'])        
        
        return embed_token

    
    def get_request_header(self):
        '''Get Power BI API request header

        Returns:
            Dict: Request header
        '''

        return {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + AadService.get_access_token()}
    
