from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "nikki",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}


def clean_scooter():
    df = pd.read_csv("/opt/airflow/data/scooter.csv")
    df.drop(columns=["region_id"], inplace=True)
    df.columns = [x.lower() for x in df.columns]
    df["started_at"] = pd.to_datetime(df["started_at"], format="%m/%d/%Y %H:%M")
    df.to_csv("/opt/airflow/data/cleanscooter.csv")


def filter_data():
    df = pd.read_csv("/opt/airflow/data/cleanscooter.csv")
    fromd = "2019-05-23"
    tod = "2019-06-03"
    tofrom = df[(df["started_at"] > fromd) & (df["started_at"] < tod)]
    tofrom.to_csv("/opt/airflow/data/may23-june3.csv")


with DAG(
    dag_id="clean_scooter_data",
    description="Clean and filter scooter data",
    default_args=default_args,
    start_date=datetime(2023, 9, 12),
    schedule="@daily",
) as dag:
    cleanData = PythonOperator(
        task_id="clean",
        python_callable=clean_scooter,
    )

    selectData = PythonOperator(
        task_id="filter",
        python_callable=filter_data,
    )

    copyFile = BashOperator(
        task_id="copy",
        bash_command="cp /opt/airflow/data/may23-june3.csv /opt/airflow/logs",
    )

    cleanData >> selectData >> copyFile
