#!/bin/bash

prefect server start &
sleep 15
python database/database_connection.py &
sleep 15
streamlit run Home.py --server.port=8501 --server.address=0.0.0.0

