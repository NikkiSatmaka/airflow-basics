from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from sklearn.model_selection import train_test_split

default_args = {
    "owner": "nikki",
    "retries": 5,
    "retry_interval": timedelta(minutes=5),
}


def impute_na(df, variable, mean_value, median_value):
    df[variable + "_mean"] = df[variable].fillna(mean_value)
    df[variable + "_median"] = df[variable].fillna(median_value)
    df[variable + "_zero"] = df[variable].fillna(0)

    return df


def split_train_test():
    data_titanic = pd.read_csv("/opt/airflow/data/Titanic.csv")
    X_train_titanic, X_test_titanic, y_train_titanic, y_test_titanic = train_test_split(
        data_titanic, data_titanic["Survived"], test_size=0.3, random_state=0
    )

    X_train_titanic.to_csv("/opt/airflow/data/Titanic_X_train_titanic.csv")
    X_test_titanic.to_csv("/opt/airflow/data/Titanic_X_test_titanic.csv")
    y_train_titanic.to_csv("/opt/airflow/data/Titanic_y_train_titanic.csv")
    y_test_titanic.to_csv("/opt/airflow/data/Titanic_y_test_titanic.csv")


def impute_age():
    X_train_titanic = pd.read_csv("/opt/airflow/data/Titanic_X_train_titanic.csv")
    X_test_titanic = pd.read_csv("/opt/airflow/data/Titanic_X_test_titanic.csv")
    mean_titanic_age = X_train_titanic["Age"].mean()
    median_titanic_age = X_train_titanic["Age"].median()

    X_train_titanic = impute_na(
        X_train_titanic, "Age", mean_titanic_age, median_titanic_age
    )
    X_test_titanic = impute_na(
        X_test_titanic, "Age", mean_titanic_age, median_titanic_age
    )
    X_train_titanic.to_csv("/opt/airflow/data/Titanic_X_train_imputed.csv")
    X_test_titanic.to_csv("/opt/airflow/data/Titanic_X_test_imputed.csv")


with DAG(
    dag_id="cleaning_titanic_v01",
    description="imputing missing data",
    default_args=default_args,
    start_date=datetime(2023, 9, 13),
    schedule="@daily",
) as dag:
    task_split_train_test = PythonOperator(
        task_id="split_train_test", python_callable=split_train_test
    )

    task_impute_age = PythonOperator(task_id="impute_age", python_callable=impute_age)

    task_split_train_test >> task_impute_age
