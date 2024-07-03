FROM python:3.10-bullseye
# ENV TZ=Europe/Madrid
WORKDIR /usr/src/app
# Copy files
# COPY data/db_download data/db_download
COPY pages pages
COPY images images
COPY models models
COPY services services
COPY utils.py utils.py
COPY Home.py Home.py
COPY database/database_connection.py database/database_connection.py
COPY database/tuya_connection.py database/tuya_connection.py
COPY style.css style.css
# COPY .env .env
COPY config.yaml config.yaml
COPY requirements.txt requirements.txt
# COPY start.sh start.sh
# Install requirements
RUN pip install -r requirements.txt
# Expose Streamlit app port
EXPOSE 8501
EXPOSE 4200
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ADD start.sh /
RUN chmod +x /start.sh
CMD ["/start.sh"]
# ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
