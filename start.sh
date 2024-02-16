#!/bin/bash

prefect server start &
sleep 10
python database/database_connection.py &
sleep 10
streamlit run Home.py --server.port=8501 --server.address=0.0.0.0

