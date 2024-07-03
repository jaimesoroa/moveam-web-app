# Standard library imports
import json
from  datetime import datetime, date, timedelta
import os

# Third-party imports
import pandas as pd
import numpy as np
import calendar
import time
import boto3
from botocore.exceptions import ClientError
import logging
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
import sqlalchemy as db
from sqlalchemy.pool import QueuePool
from prefect import task, flow
from prefect.server.schemas.schedules import CronSchedule
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, before_sleep_log

# ==============================================================================================
# Retry logic

# Define the retry decorator
retry_decorator = retry(
    stop=stop_after_attempt(3),  # Retry up to 3 times
    wait=wait_fixed(2),  # Wait 2 seconds between retries
    retry=retry_if_exception_type(Exception),  # Retry on any exception
    before_sleep=before_sleep_log(__name__, "info")  # Log before each retry, good for debugging.
)


# AWS secrets

@task(log_prints=True)
def get_secret_tuya():

    secret_name = "Tuya_platform"
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

    secret = get_secret_value_response['SecretString']
    
    return json.loads(secret)

# Database secrets to access database

@task(log_prints=True)
def get_secrets_database():

    secret_name = "db_tarragona_historico_Jaime"
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
    
    return json.loads(secret)

# Update Prefect config to use MySQL instead of SQLite
# Not used for the moment, trying to make SQLite internal DB work.

@task(log_prints=True)
def update_prefect_config(secrets, db_name):

    # Update Prefect configuration
    os.environ["PREFECT_ORION_DATABASE_CONNECTION_URL"] = (
        f"mysql+pymysql://{secrets['username']}:{secrets['password']}@"
        f"{secrets['host']}:{secrets.get('port', 3306)}/{db_name}"
    )
        
    return None

# Launch Tuya API connection

@task(log_prints=True)
@retry_decorator
def tuya_api_conection(tuya_secrets):
    # API parameters

    ACCESS_ID =  tuya_secrets['Tuya_access_id']
    ACCESS_SECRET = tuya_secrets['Tuya_access_secret']
    API_ENDPOINT = "https://openapi.tuyaeu.com"
    # MQ_ENDPOINT = "wss://mqe.tuyaeu.com:8285/"

    # Enable debug log
    # TUYA_LOGGER.setLevel(logging.DEBUG)
    TUYA_LOGGER.setLevel(logging.NOTSET)

    # Init OpenAPI and connect
    openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_SECRET)
    openapi.connect()
    
    return openapi

# Device list

@task(log_prints=True)
@retry_decorator
def get_devices(openapi):
    params ={
        'page_size': '20',
        'last_id': ''
    }
    
    device_list = []
    
    response = openapi.get(f'/v2.0/cloud/thing/device', params)
    result = response['result']
    for device in result:
        device_list.append(device['id'])
        
    while len(result) > 0:
        params ={
        'page_size': '20',
        'last_id': result[-1]['id']
        }
        response = openapi.get(f'/v2.0/cloud/thing/device', params)
        result = response['result']
        for device in result:
            device_list.append(device['id'])
            
    return device_list

# Get device report logs

def get_report_logs(openapi, codes, start_time, end_time, last_row_key, device_id):
    params = {
        'codes': codes,
        'start_time': start_time,
        'end_time': end_time,
        'last_row_key': last_row_key,
        "size": '100'
        }
    response = openapi.get("/v2.0/cloud/thing/{}/report-logs".format(device_id), params)
    
    log_list = []
    has_more = False
    if 'result' in response:
        if 'logs' in response['result']:
            log_list = list(response['result']['logs'])
            datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for log in log_list:
                log['device_id'] = response['result']['device_id']
                log['event_date_time'] = datetime.fromtimestamp(int(log['event_time'])/1000).strftime('%Y-%m-%d %H:%M:%S')
                log['last_updated'] = datetime_now
        
        has_more = response['result']['has_more']
        if has_more == True:
            last_row_key = response['result']['last_row_key']
    
    return log_list, has_more, last_row_key

# Extract all logs for a list of devices

@task(log_prints=True)
@retry_decorator
def log_extraction(device_list, openapi):

    event_list = []
    previous_day = date.today()-timedelta(1)
    year = int(previous_day.strftime('%Y'))
    month = int(previous_day.strftime('%m'))
    day = int(previous_day.strftime('%d'))
    codes = ('switch,temp_set,temp_current,level,child_lock,fault,sleep')

    for device_id in device_list:
        # First day of each month
        start_time = str(int(datetime(year, month, day, 0, 0, 0).timestamp()*1000))
        # Last day of each month
        end_time = str(int(datetime(year, month, day, 23, 59, 59, 999999).timestamp()*1000))
        last_row_key = ''

        (report_log_list, has_more, last_row_key) = get_report_logs(openapi, codes, start_time, end_time, last_row_key, device_id)
        event_list.extend(report_log_list)

        while has_more == True:
            (report_log_list, has_more, last_row_key) = get_report_logs(openapi, codes, start_time, end_time, last_row_key, device_id)
            event_list.extend(report_log_list)
    
    return event_list

# Writing of the logs in the database

@task(log_prints=True)
@retry_decorator
def database_writing(username, password, host, database, df):
    url_object = db.URL.create(
        "mysql+mysqldb",
        username=username,
        password=password,
        host=host,
        database=database,
    )

    engine = db.create_engine(url_object, pool_pre_ping=True)
    
    db_table = 'termostatos'
    
    try:
        with engine.begin() as conn:
                # Insert whole DataFrame into MySQL
                df.to_sql(db_table, con=engine, if_exists='append', chunksize=2000, index=False)
                print(f'DataFrame written in database at {datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")}')
    except Exception as e:
        print(f"An error occurred when trying to write in database: {e}")
    finally:
        engine.dispose()
    
    return None

@flow(name="tuya-connection-flow", log_prints=True)
def tuya_flow():
    tuya_secrets = get_secret_tuya()
    database_secrets = get_secrets_database()
    # update_prefect_config(database_secrets, 'StayTarragona')
    openapi = tuya_api_conection(tuya_secrets)
    device_list = get_devices(openapi)
    event_list = log_extraction(device_list, openapi)
    df = pd.DataFrame(event_list)
    database_writing(database_secrets['username'], database_secrets['password'], database_secrets['host'], 'StayTarragona', df)

    return None


if __name__ == "__main__":
    
    # Create a deployment for the flow
    # deployment = tuya_flow.deploy(
    #     name="datadis-deployment",
    #     schedules=[CronSchedule(cron="0 5 * * *", timezone="UTC")],  # Adjust the cron expression as needed
    #     tags=["datadis"]
    # )
    
    # Create a deployment for the flow
    tuya_deployment = tuya_flow.serve(
        name="tuya-deployment",
        cron="0 5 * * *", # Adjust the cron expression as needed
        tags= ['tuya']
        )

    # Register the deployment
    tuya_deployment.apply()
