FROM apache/airflow:2.7.1-python3.11
COPY --chown=$AIRFLOW_UID:0 requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt
