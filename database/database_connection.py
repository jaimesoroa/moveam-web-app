# Standard library imports
import os
import json
from datetime import datetime
import logging

# Third-party imports
import pandas as pd
import requests
import sqlalchemy as db
from sqlalchemy import MetaData, delete, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import boto3
from botocore.exceptions import ClientError
from prefect import task, flow, serve  # , get_client
from prefect.client.orchestration import PrefectClient
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from prefect.deployments import Deployment
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


# @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
# def execute_with_retry(conn, statement):
#     conn.execute(statement)

# ==============================================================================================
# AWS secrets

# AWS secrets Datadis
@task(log_prints=True)
def get_secret_datadis():

    secret_name = "Datadis_connection"
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
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    return json.loads(secret)

# AWS secrets Database
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

# AWS secrets Prefect
# @task(log_prints=True)
# @flow(name="prefect-secrets-flow", log_prints=True)
def get_secrets_prefect():

    secret_name = "Movam_app_PrefectCloud"
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

# ==============================================================================================
# Update Prefect config to use MySQL instead of SQLite
# Not used for the moment, trying to make SQLite internal DB work.

@task(log_prints=True)
def update_prefect_config(secrets, db_name):

    # Update Prefect configuration
    os.environ["PREFECT_API_DATABASE_CONNECTION_URL"] = (
        f"mysql+pymysql://{secrets['username']}:{secrets['password']}@"
        f"{secrets['host']}:{secrets.get('port', 3306)}/{db_name}"
    )
        
    return None

# ==============================================================================================
# Create a persistent engine at the module level

def create_module_engine(username, password, host, database):
    engine = create_engine(
        db.URL.create(
            "mysql+mysqldb",
            username=username,
            password=password,
            host=host,
            database=database,
        ),
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True
    )

    Session = sessionmaker(bind=engine)
    
    return engine, Session

# ==============================================================================================
# Datadis connection

@task(log_prints=True)
@retry_decorator
def datadis_connection(username, password, authorized_nif):
    # Datos Moveam de Stay
    data_moveam = {'username':username,
            'password':password
            }
    API_ENDPOINT = "https://datadis.es/nikola-auth/tokens/login"
    token_moveam = requests.post(url = API_ENDPOINT, data = data_moveam)

    headers_moveam = {"Authorization": f'Bearer {token_moveam.text}'}

    # Supplies Cordoba CUPS
    supplies_params = {
        "authorizedNif": authorized_nif
    }

    supplies_response = requests.get("https://datadis.es/api-private/api/get-supplies", params= supplies_params, headers= headers_moveam)
    return headers_moveam, supplies_response

# ==============================================================================================
# Whole CUPS list
@task(log_prints=True)
@retry_decorator
def whole_cups_list(supplies_response):
    cups_list= []
    supplies_response_dict = json.loads(supplies_response.text)
    for supply in supplies_response_dict:
        cups_list.append(supply['cups'])
    return cups_list

@task(log_prints=True)
def cups_month():
    current_month = datetime.today().strftime('%m')
    current_day = datetime.today().strftime('%d')
    if current_month == '01':
        previous_month = '12'
    else:
        previous_month = str(int(current_month)-1)
    if int(current_day) <= 3:
        if len(current_month) == 1 and len(previous_month) == 1:
            months = [f'0{previous_month}',f'0{current_month}']
        elif len(current_month) > 1 and len(previous_month) == 1:
            months = [f'0{previous_month}', current_month]
        elif len(current_month) == 1 and len(previous_month) > 1:
            months = [previous_month,f'0{current_month}']
        else:
            months = [previous_month, current_month]
    else:
        if len(current_month) == 1:
            months = [f'0{current_month}']
        else:
            months = [current_month]
    return months

# ==============================================================================================
# Database connection
# @task(log_prints=True) # This is not a task, it's called by a task
def database_connection(cups, username, password, host, database, month, df, year, db_table):
    url_object = db.URL.create(
        "mysql+mysqldb",
        username=username,
        password=password,
        host=host,
        database=database,
    )

    # Previous command
    # engine = db.create_engine(url_object, pool_pre_ping=True)
    # New command to avoid SQLite error.
    engine = db.create_engine(url_object, poolclass=QueuePool, pool_size=10, max_overflow=20, pool_pre_ping=True)
    
    try:
        # Initialize the Metadata Object
        META_DATA = MetaData()
        MetaData.reflect(META_DATA, bind=engine)
        ELECTRICIDAD = META_DATA.tables[db_table]
        
        # Use a single transaction for all deletions
        with engine.begin() as conn:
            # Check if there has already been an update today.
            sql = f'select * from ELECTRICIDAD where month = {month} and year = {year} and cups = "{cups}"'
            df = pd.read_sql(sql,con=engine)
            if len(df) == 0 or (df['lastUpdated'][0].strftime('%Y-%m-%d') != datetime.today().strftime('%Y-%m-%d')):
                # Delete the previously updated month (before today)
                dele = ELECTRICIDAD.delete().where(ELECTRICIDAD.c.month == int(month)).where(ELECTRICIDAD.c.cups == cups).where(ELECTRICIDAD.c.year == int(year))
                conn.execute(dele)
                print(f'Month {month} deleted for CUPS {cups} at {datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")}')
                
                # Insert whole DataFrame into MySQL
                df.drop_duplicates(subset=['cups', 'date', 'time', 'month', 'year'], keep='last', inplace=True, ignore_index=True)
                df.to_sql('ELECTRICIDAD', con=engine, if_exists='append', chunksize=2000, index=False)
                print(f'DataFrame from CUPS {cups} and month {month} written in database at {datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")}')
            else:
                print(f'CUPS {cups} has already been updated at {datetime.today().strftime("%Y-%m-%d")}')
    except Exception as e:
        print(f"An error occurred for CUPS {cups} when trying to delete and write in database: {e}")
    finally:
        engine.dispose()
    
    return None

# This is not a task, it's called by a task
def database_month_deletion(month_cups_list, engine, Session, month, year, db_table):
    # url_object = db.URL.create(
    #     "mysql+mysqldb",
    #     username=username,
    #     password=password,
    #     host=host,
    #     database=database,
    # )
    
    session = Session()

    # Previous command
    # engine = db.create_engine(url_object, pool_pre_ping=True)
    # New command to avoid SQLite error.
    # engine = db.create_engine(url_object, poolclass=QueuePool, pool_size=10, max_overflow=20, pool_pre_ping=True)
    
    try:
        for cups in month_cups_list:
            META_DATA = MetaData()
            MetaData.reflect(META_DATA, bind=engine)
            ELECTRICIDAD = META_DATA.tables[db_table]
            # Use a single transaction for all deletions
            # with engine.begin() as conn:
            with session.begin():
                dele = ELECTRICIDAD.delete().where(ELECTRICIDAD.c.month == int(month)).where(ELECTRICIDAD.c.year == int(year)).where(ELECTRICIDAD.c.cups == cups)
                # conn.execute(dele)
                session.execute(dele)
            # engine.dispose()
    except Exception as e:
        print(f"An error occurred for CUPS {cups}, month {month} and year {year} when trying to delete in database: {e}")
    finally:
        # engine.dispose()
        session.close()
    
    return None

# This is not a task, it's called by a task
# def database_writing(username, password, host, database, month, df, year, db_table):
def database_writing(engine, Session, month, df, year, db_table):
    # url_object = db.URL.create(
    #     "mysql+mysqldb",
    #     username=username,
    #     password=password,
    #     host=host,
    #     database=database,
    # )
    
    session = Session()

    # Previous command
    # engine = db.create_engine(url_object, pool_pre_ping=True)
    # New command to avoid SQLite error.
    # engine = db.create_engine(url_object, poolclass=QueuePool, pool_size=10, max_overflow=20, pool_pre_ping=True)
    
    try:
        # Use a single transaction for all deletions
        # with engine.begin() as conn:
        with session.begin():
                # Insert whole DataFrame into MySQL
                df.to_sql(db_table, con=engine, if_exists='append', chunksize=2000, index=False)
                print(f'DataFrame from month {month} and year {year} written in database at {datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")}')
    except Exception as e:
        print(f"An error occurred for month {month} and year {year} when trying to write in database: {e}")
    finally:
        # engine.dispose()
        session.close()
    
    return None

# ==============================================================================================
# Download consumption from Datadis
@task(log_prints=True)
@retry_decorator
# def consumption(months, cups_list, headers_moveam, username, password, host, database, db_table, authorized_nif, distributorCode):
def consumption(months, cups_list, headers_moveam, engine, Session, db_table, authorized_nif, distributorCode):
    status_code_list = []
    current_year = datetime.today().strftime('%Y')
    previous_year = str(int(current_year)-1)
    all_data = []
    for month in months:
        month_data = []
        year = previous_year if len(months) == 2 and month == months[0] and month == '12' else current_year
        for cups in cups_list:
            consumption_params = {
            "cups": cups,
            "distributorCode": distributorCode,
            "startDate": f'{year}/{month}',
            "endDate": f'{year}/{month}',
            "measurementType": "0",
            "measurePointType": "5",
            "pointType": "5",
            "authorizedNif": authorized_nif
            }
            # API request
            try:
                response = requests.get("https://datadis.es/api-private/api/get-consumption-data",
                                        params= consumption_params,
                                        headers= headers_moveam
                                        )
                status_code_list.append(response.status_code)
                print(f'CUPS {cups} has a response code of {response.status_code}')

                # Only use valid responses            
                if response.status_code == 200 and len(response.text) > 3:
                    # Extract the response data and create a dataframe
                    data = response.json()  # Use json() instead of eval
                    df = pd.DataFrame(data, index= None).drop(columns=['obtainMethod', 'surplusEnergyKWh'])
                    df['month'] = pd.to_datetime(df['date']).dt.month
                    df['year'] = pd.to_datetime(df['date']).dt.year
                    current_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')
                    df['lastUpdated'] = current_datetime

                    # Include the dataframe in a list of dataframes to use later to write in the database
                    all_data.append(df)
                    month_data.append(df)
                
            except Exception as e:
                print(f"An error occurred for CUPS {cups}: {e}")
                
        if len(month_data) > 0:
            month_df = pd.concat(month_data)
            # month_df.drop_duplicates(subset=['cups', 'date', 'time', 'month', 'year'], keep='last', inplace=True, ignore_index=True)
            month_cups_list = month_df['cups'].unique()
            database_month_deletion(month_cups_list, engine, Session, month, year, db_table)

    if len(all_data) > 0:
        final_df = pd.concat(all_data)
        final_df.drop_duplicates(subset=['cups', 'date', 'time', 'month', 'year'], keep='last', inplace=True, ignore_index=True)
    else:
        final_df = pd.DataFrame()
    
    database_writing(engine, Session, month, final_df, year, db_table)
    
    return final_df


@flow(name="datadis-connection-flow", log_prints=True)
def datadis_flow():
    
    datadis_secrets = get_secret_datadis()
    database_secrets = get_secrets_database()
    months = cups_month()
    
    # Cordoba process
    (headers_moveam_cordoba, supplies_response_cordoba) = datadis_connection(
        datadis_secrets['datadis_username'],
        datadis_secrets['datadis_password'],
        datadis_secrets['datadis_authorized_nif_cordoba']
        )
    
    cups_list_cordoba = whole_cups_list(supplies_response_cordoba)
    
    # update_prefect_config(database_secrets, database_secrets['dbname_cordoba'])
    (engine_cordoba, session_cordoba) = create_module_engine(
        database_secrets['username'],
        database_secrets['password'],
        database_secrets['host'],
        database_secrets['dbname_cordoba']
        )
    
    consumption_df_cordoba = consumption(
        months,
        cups_list_cordoba,
        headers_moveam_cordoba,
        engine_cordoba,
        session_cordoba,
        'ELECTRICIDAD',
        datadis_secrets['datadis_authorized_nif_cordoba'],
        '2'
        )
    
    # consumption_df_cordoba = consumption(months, cups_list_cordoba, headers_moveam_cordoba, database_secrets['username'], database_secrets['password'], 
    #     database_secrets['host'], database_secrets['dbname_cordoba'], 'ELECTRICIDAD', datadis_secrets['datadis_authorized_nif_cordoba'], '2')
    
    # Torrejón process
    (headers_moveam_torrejon, supplies_response_torrejon) = datadis_connection(
        datadis_secrets['datadis_username'],
        datadis_secrets['datadis_password'],
        datadis_secrets['datadis_authorized_nif_torrejon']
        )
    
    cups_list_torrejon = whole_cups_list(supplies_response_torrejon)
    
    (engine_torrejon, session_torrejon) = create_module_engine(
        database_secrets['username'],
        database_secrets['password'],
        database_secrets['host'],
        database_secrets['dbname_torrejon']
        )
    
    consumption_df_torrejon = consumption(
        months,
        cups_list_torrejon,
        headers_moveam_torrejon,
        engine_torrejon,
        session_torrejon,
        'ELECTRICIDAD_DATADIS',
        datadis_secrets['datadis_authorized_nif_torrejon'],
        '8'
        )
        
    return consumption_df_cordoba, consumption_df_torrejon

    
# Connection to Prefect cloud, not used for the moment.
async def cloud_connection(prefect_api_url, prefect_api_key, prefect_tenant_id, cordoba_flow):
    # Register the flow using the Prefect API
    async with PrefectClient(api= prefect_api_url, api_key= prefect_api_key) as client:
        
        # Create a flow run reference by serializing the flow instance
        cordoba_flow_reference = await client.create_flow(flow= cordoba_flow)
        # Print the flow run ID for reference
        
        # Create a flow run reference by serializing the flow instance
        cordoba_flow_deployment = await client.create_deployment(flow_id= cordoba_flow_reference, name= "cordoba-flow-deployment",
                                                         schedule= {'cron': "0 3 * * *", 'timezone': "Europe/Madrid"}
        )
        # Create a flow run reference by serializing the flow instance
        cordoba_flow_run = await client.create_flow_run_from_deployment(deployment_id= cordoba_flow_deployment
        )
        # flow_run = await client.create_flow_run(flow= cordoba_flow
        # )
        
    return cordoba_flow_run


if __name__ == "__main__":
    
    # Create a deployment for the flow
    datadis_deployment = datadis_flow.serve(
        name="datadis-deployment",
        cron="0 6 * * *", # Adjust the cron expression as needed
        tags= ['datadis']
        )

    # Register the deployment
    datadis_deployment.apply()
    