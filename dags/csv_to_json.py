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


def csv_to_json():
    df = pd.read_csv("/opt/airflow/data/data.csv")
    for i, r in df.iterrows():
        print(r["name"])
    df.to_json("/opt/airflow/data/fromAirflow.json", orient="records")


with DAG(
    dag_id="csv_to_json",
    description="Convert data.csv to fromAirflow.json",
    default_args=default_args,
    start_date=datetime(2023, 9, 12),
    schedule="@daily",
) as dag:
    print_starting = BashOperator(
        task_id="starting",
        bash_command='echo "I am reading the CSV now....."',
    )

    task_csv_to_json = PythonOperator(
        task_id="convert_csv_to_json",
        python_callable=csv_to_json,
    )

    print_starting >> task_csv_to_json
