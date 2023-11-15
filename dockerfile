FROM python:3.10-bullseye
WORKDIR /usr/src/app
# Copy files
COPY data/db_download data/db_download
COPY pages pages
COPY images images
COPY Home.py Home.py
COPY database database
COPY style.css style.css
COPY .env .env
COPY config.yaml config.yaml
COPY requirements.txt requirements.txt
COPY start.sh start.sh
# Install requirements
RUN pip install -r requirements.txt
# Expose Streamlit app port
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ADD start.sh /
RUN chmod +x /start.sh
CMD ["/start.sh"]