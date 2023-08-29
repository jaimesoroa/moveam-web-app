FROM python:3.10-slim
WORKDIR /moveam_app
COPY moveam_app moveam_app
COPY .env .env
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "moveam_app/Home.py", "--server.port=8501", "--server.address=0.0.0.0"]