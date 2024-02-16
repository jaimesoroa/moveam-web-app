import pandas as pd
# import os
import requests
import sqlalchemy as db
from sqlalchemy import MetaData, delete
from datetime import datetime
# import datetime as dt
import boto3
from botocore.exceptions import ClientError
# import asyncio
# import prefect
from prefect import task, flow, serve#, get_client
# from prefect.client.cloud import CloudClient
from prefect.client.orchestration import PrefectClient
# from prefect.schedules import CronSchedule
import json

# Get the parent directory
# parent_dir = os.path.dirname(os.path.realpath(__file__))

# # ==============================================================================================
# # AWS secrets

# # Tarragona database secrets
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
#         raise e

#     # Decrypts secret using the associated KMS key.
#     secret = get_secret_value_response['SecretString']

#     return eval(secret)

# # ==============================================================================================
# # Connect to database

# def tarragona_connection(SQL_DB_TARRAGONA_USER, SQL_DB_TARRAGONA_PWD, SQL_DB_TARRAGONA_SERVER, 
#   SQL_DB_TARRAGONA_DB):
#     url_db_tarragona = db.URL.create(
#         "mysql+mysqldb",
#         username = SQL_DB_TARRAGONA_USER,
#         password = SQL_DB_TARRAGONA_PWD,
#         host = SQL_DB_TARRAGONA_SERVER,
#         database = SQL_DB_TARRAGONA_DB,
#     )

#     tarragona_db_engine = db.create_engine(url_db_tarragona)
#     print('Connected to database')

#     with tarragona_db_engine.connect() as conn, conn.begin():
#         data_tarragona = pd.read_sql_table("kWh", conn)
#     print('Data downloaded')
        
#     # Find a way to add only the new lines, instead of the whole table
    
#     # Save the DataFrame as a CSV file locally
#     data_tarragona.to_csv("xxx.csv", index=False)
#     print('CSV written')
    
#     return data_tarragona


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
# Datadis connection

@task(log_prints=True)
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
# @task(log_prints=True)
def database_connection(cups, username, password, host, database, month, df, year):
    url_object = db.URL.create(
        "mysql+mysqldb",
        username=username,
        password=password,
        host=host,
        database=database,
    )

    engine = db.create_engine(url_object, pool_pre_ping=True)
    
    try:
        # Initialize the Metadata Object
        META_DATA = MetaData()
        MetaData.reflect(META_DATA, bind=engine)
        ELECTRICIDAD = META_DATA.tables['ELECTRICIDAD']
        
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

def database_month_deletion(month_cups_list, username, password, host, database, month, year):
    url_object = db.URL.create(
        "mysql+mysqldb",
        username=username,
        password=password,
        host=host,
        database=database,
    )

    engine = db.create_engine(url_object, pool_pre_ping=True)
    
    try:
        for cups in month_cups_list:
            META_DATA = MetaData()
            MetaData.reflect(META_DATA, bind=engine)
            ELECTRICIDAD = META_DATA.tables['ELECTRICIDAD']
            # Use a single transaction for all deletions
            with engine.begin() as conn:
                dele = ELECTRICIDAD.delete().where(ELECTRICIDAD.c.month == int(month)).where(ELECTRICIDAD.c.year == int(year)).where(ELECTRICIDAD.c.cups == cups)
                conn.execute(dele)
            # engine.dispose()
    except Exception as e:
        print(f"An error occurred for CUPS {cups}, month {month} and year {year} when trying to delete in database: {e}")
    finally:
        engine.dispose()
    
    return None

def database_writing(username, password, host, database, month, df, year):
    url_object = db.URL.create(
        "mysql+mysqldb",
        username=username,
        password=password,
        host=host,
        database=database,
    )

    engine = db.create_engine(url_object, pool_pre_ping=True)
    
    try:
        # Use a single transaction for all deletions
        with engine.begin() as conn:
                # Insert whole DataFrame into MySQL
                df.to_sql('ELECTRICIDAD', con=engine, if_exists='append', chunksize=2000, index=False)
                print(f'DataFrame from month {month} and year {year} written in database at {datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")}')
    except Exception as e:
        print(f"An error occurred for month {month} and year {year} when trying to write in database: {e}")
    finally:
        engine.dispose()
    
    return None

# ==============================================================================================
# Download consumption from Datadis
@task(log_prints=True)
def consumption(months, cups_list, headers_moveam, username, password, host, database):
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
            "distributorCode": "2",
            "startDate": f'{year}/{month}',
            "endDate": f'{year}/{month}',
            "measurementType": "0",
            "measurePointType": "5",
            "pointType": "5",
            "authorizedNif": 'B88590583'
            }
            # API request
            try:
                response = requests.get("https://datadis.es/api-private/api/get-consumption-data", params= consumption_params, headers= headers_moveam)
                status_code_list.append(response.status_code)
                print(f'CUPS {cups} has a response code of {response.status_code}')
            except Exception as e:
                print(f"An error occurred for CUPS {cups}: {e}")
            # Only use valid responses            
            if response.status_code == 200 and len(response.text) > 3:
                # Extract the response data and create a dataframe
                data = response.json()  # Use json() instead of eval
                df = pd.DataFrame(data, index= None).drop(columns=['obtainMethod', 'surplusEnergyKWh'])
                df['month'] = pd.to_datetime(df['date']).dt.month
                df['year'] = pd.to_datetime(df['date']).dt.year
                current_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')
                df['lastUpdated'] = current_datetime
                # df.drop_duplicates(inplace=True)
                
                # Write the dataframe in the MySQL database
                # database_connection(cups, username, password, host, database, month, df, year)
                
                # Include the dataframe in a list of dataframe for when we need to check the function
                all_data.append(df)
                month_data.append(df)
                
        if len(month_data) > 0:
            month_df = pd.concat(month_data)
            month_df.drop_duplicates(subset=['cups', 'date', 'time', 'month', 'year'], keep='last', inplace=True, ignore_index=True)
            month_cups_list = month_df['cups'].unique()
            database_month_deletion(month_cups_list, username, password, host, database, month, year)
            

    if len(all_data) > 0:
        final_df = pd.concat(all_data)
        final_df.drop_duplicates(subset=['cups', 'date', 'time', 'month', 'year'], keep='last', inplace=True, ignore_index=True)
    else:
        final_df = pd.DataFrame()
    
    database_writing(username, password, host, database, month, final_df, year)
    
    return final_df


@flow(name="cordoba-connection-flow", log_prints=True)
def cordoba_flow():
    
    datadis_secrets = get_secret_datadis()
    database_secrets = get_secrets_database()
    (headers_moveam, supplies_response) = datadis_connection(datadis_secrets['datadis_username'], 
                datadis_secrets['datadis_password'], datadis_secrets['datadis_authorized_nif'])
    
    cups_list = whole_cups_list(supplies_response)

    months = cups_month()
    
    consumption_df = consumption(months, cups_list, headers_moveam, database_secrets['username'], database_secrets['password'], 
        database_secrets['host'], database_secrets['dbname_cordoba'])
    
    return consumption_df
    
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
    
    # Authenticate with Prefect Cloud using environment variables
    # prefect_secrets = get_secrets_prefect()
    # prefect_api_url = prefect_secrets['base_url']
    # prefect_api_key = prefect_secrets['api_key_nov_23']
    # prefect_tenant_id = prefect_secrets['user_id']
    # print('Prefect secrets obtained')
    
    # asyncio.run(cloud_connection(prefect_api_url, prefect_api_key, prefect_tenant_id, cordoba_flow))

    # Run the Prefect flow
    cordoba_deploy= cordoba_flow.to_deployment(name="cordoba-first-deployment", cron= '00 11 * * *')#, work_pool_name= 'cordoba_pool', work_queue_name= 'cordoba_queue')
    serve(cordoba_deploy)
    
    # To serve several flows at once:

    # To serve one flow:
    # cordoba_flow.serve(name="cordoba-first-deployment",
    #                   interval=60)
    