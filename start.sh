#!/bin/bash

prefect server start --host 0.0.0.0 &
sleep 20
# Register and schedule the deployments
python database/database_connection.py &
sleep 10
python database/tuya_connection.py &
sleep 10
# Ensure the deployments are registered before starting other services
python -c "from database.database_connection import datadis-deployment; datadis_deployment.apply()" &
sleep 10
python -c "from database.tuya_connection import tuya-deployment; tuya_deployment.apply()" &
sleep 10
# Start a Prefect worker to execute the flows
prefect worker start -q "default" &
sleep 10
streamlit run Home.py --server.port=8501 --server.address=0.0.0.0

