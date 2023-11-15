import sqlalchemy as db
import os
import pandas as pd
import asyncio
import boto3
from botocore.exceptions import ClientError
from prefect.client.orchestration import PrefectClient
import asyncio

# Get the parent directory
parent_dir = os.path.dirname(os.path.realpath(__file__))

# ===============================================================================================================
# AWS secrets

# Tarragona database secrets
def get_secret_tarragona_db():

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
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    return eval(secret)

# ===============================================================================================================
# Connect to database

def tarragona_connection(SQL_DB_TARRAGONA_USER, SQL_DB_TARRAGONA_PWD, SQL_DB_TARRAGONA_SERVER, SQL_DB_TARRAGONA_DB):
    url_db_tarragona = db.URL.create(
        "mysql+mysqldb",
        username = SQL_DB_TARRAGONA_USER,
        password = SQL_DB_TARRAGONA_PWD,
        host = SQL_DB_TARRAGONA_SERVER,
        database = SQL_DB_TARRAGONA_DB,
    )

    tarragona_db_engine = db.create_engine(url_db_tarragona)
    print('Connected to database')

    with tarragona_db_engine.connect() as conn, conn.begin():
        data_tarragona = pd.read_sql_table("kWh", conn)
    print('Data downloaded')
        
    # Find a way to add only the new lines, instead of the whole table
    
    # Save the DataFrame as a CSV file locally
    data_tarragona.to_csv("/Users/jaimesoroarubio/code/work_projects/Moveam/moveam-web-app/data/db_download/kWh_tarragona.csv", index=False)
    print('CSV written')
    
    return data_tarragona
    
    
if __name__ == "__main__":
    tarragona_secrets = get_secret_tarragona_db()
    SQL_DB_TARRAGONA_USER = tarragona_secrets['username']
    SQL_DB_TARRAGONA_PWD = tarragona_secrets['password']
    SQL_DB_TARRAGONA_SERVER = tarragona_secrets['host']
    SQL_DB_TARRAGONA_DB = tarragona_secrets['dbname']
    tarragona_connection(SQL_DB_TARRAGONA_USER, SQL_DB_TARRAGONA_PWD, SQL_DB_TARRAGONA_SERVER, SQL_DB_TARRAGONA_DB)

    