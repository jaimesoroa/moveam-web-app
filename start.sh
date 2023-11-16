#!/bin/bash

# Run Prefect flow
# prefect agent start -p 'default-agent-pool' &

# Wait for Prefect flow to start (you might need to adjust the sleep duration)
# sleep 10

# Run Streamlit app
streamlit run Home.py --server.port=8501 --server.address=0.0.0.0

