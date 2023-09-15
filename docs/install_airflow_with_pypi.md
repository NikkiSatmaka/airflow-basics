# Installing Airflow using pypi


```bash
docker run -it --rm -p 8080:8080 python:3.11-slim /bin/bash
```
* Create and start a docker container from the Docker image python:3.11-slim and execute the command /bin/bash in order to have a shell session


```bash
python -V
```
* Print the Python version


```bash
export AIRFLOW_HOME=/opt/airflow
```
* Export the environment variable AIRFLOW_HOME used by Airflow to store the dags folder, logs folder and configuration file


```bash
env | grep airflow
```
* To check that the environment variable has been well exported


```bash
apt-get update -y && apt-get install -y wget libczmq-dev curl libssl-dev git inetutils-telnet bind9utils freetds-dev libkrb5-dev libsasl2-dev libffi-dev libpq-dev freetds-bin build-essential default-libmysqlclient-dev apt-utils rsync zip unzip gcc && apt-get clean
```
* Install all tools and dependencies that can be required by Airflow


```bash
useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow
```
* Create the user airflow, set its home directory to the value of AIRFLOW_HOME and log into it


```bash
cat /etc/passwd | grep airflow
```
* Show the file /etc/passwd to check that the airflow user has been created


```bash
pip install --upgrade pip
```
* Upgrade pip (already installed since we use the Docker image python 3.5)


```bash
su - airflow
```
* Log into airflow


```bash
python -m venv .sandbox
```
* Create the virtual env named sandbox


```bash
source .sandbox/bin/activate
```
* Activate the virtual environment sandbox


```bash
wget https://raw.githubusercontent.com/apache/airflow/constraints-2.7.1/constraints-3.11.txt
```
* Download the requirement file to install the right version of Airflow’s dependencies


```bash
pip install "apache-airflow[celery,postgres,cncf.kubernetes,docker]"==2.7.1 --constraint ./constraints-3.11.txt
```

* Install the version 2.7.1 of apache-airflow with all subpackages defined between square brackets. (Notice that you can still add subpackages after all, you will use the same command with different subpackages even if Airflow is already installed)


```bash
airflow db migrate
```
* Set up the metadatabase (Latest schemas, values, ...)


```bash
airflow users create --username airflow --password airflow --firstname Airflow --lastname Admin --role Admin --email airflowadmin@example.com
```
* Create "airflow" user with role "Admin"


```bash
airflow scheduler &
```
* Start Airflow’s scheduler in background


```bash
airflow webserver --port 8080 &
```
* Start Airflow’s webserver in background


Quick Tour of Airflow CLI


```bash
docker ps
```
* Show running docker containers


```bash
docker exec -it container_id /bin/bash
```
* Execute the command /bin/bash in the container_id to get a shell session


```bash
su - airflow
```
* Log into airflow


```bash
source .sandbox/bin/activate
```
* Activate the virtual environment sandbox


```bash
pwd
```
* Print the current path where you are


```bash
airflow dags list
```
* Give the list of known dags (either those in the examples folder or in dags folder)


```bash
ls
```
* Display the files/folders of the current directory


```bash
airflow dags trigger example_python_operator
```
* Trigger the dag example_python_operator with the current date as execution date


```bash
airflow dags trigger example_python_operator -e 2023-01-01
```
* Trigger the dag example_python_operator with a date in the past as execution date (This won’t trigger the tasks of that dag unless you set the option catchup=True in the DAG definition)


```bash
airflow dags trigger example_python_operator -e '2023-01-01 19:04:00+00:00'
```
* Trigger the dag example_python_operator with a date in the future (change the date here with one having +2 minutes later than the current date displayed in the Airflow UI). The dag will be scheduled at that date.


```bash
airflow dags list-runs -d example_python_operator
```
* Display the history of example_python_operator’s dag runs


```bash
airflow tasks list example_python_operator
```
* List the tasks contained into the example_python_operator dag


```bash
airflow tasks test example_python_operator print_the_context 2023-01-01
```
* Allow to test a task (print_the_context) from a given dag (example_python_operator here) without taking care of dependencies and past runs. Useful for debugging.
