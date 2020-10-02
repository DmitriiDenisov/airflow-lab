# airflow-lab


## Install 
```
# airflow needs a home, ~/airflow is the default,
# but you can lay foundation somewhere else if you prefer
# (optional)
export AIRFLOW_HOME=~/airflow

# install from pypi using pip
pip install apache-airflow

# initialize the database
airflow initdb
```

## Start webserver and scheduler:

1. `airflow webserver -p 8080 -D `
2. `airflow scheduler -D`
(in case if scheduler does not run in Daemon mode try to run `sudo rm $AIRFLOW_HOME airflow-scheduler.err  airflow-scheduler.pid`)
3. Check: go to url <ip>:8080

## Stop Airflow:

1. `cat ~/airflow/airflow-webserver.pid | xargs kill -9` (will take around 30 secs to stop it)
2. (optional) To check that all stopped: `lsof -i tcp:8080`



Source: https://vujade.co/install-apache-airflow-ubuntu-18-04/

## Tutorials

1. BashOperator 
2. PythonOperator and multiple tasks in DAG
3. Show parameters of default_args in DAG (see dag_3.py)
4. Еще пример разных конструкций, см DAG test_5 и немного рассказать про dagrun_timeout=timedelta(minutes=5)
5. 
2. BranchPythonOperator (3 examples) (example_branch_dop_operator_v3_myschedule)
Source1:https://stackoverflow.com/questions/43678408/how-to-create-a-conditional-task-in-airflow
Source2: https://airflow.apache.org/docs/stable/concepts.html?highlight=xcom#branching

3. BranchPythonOperator - return list of tasks (branch_list_ex)

4. LatestOnlyOperator 1 (latest_only_ex) - вкратце, предположим есть таска t=LatestOnlyOperator(). Если DAG стартует перед текущей датой, то вместо того, чтобы все раны пропустить (catchup=False), этот оператор пропускает все разы только тех тасков, которые зависят от таски t.
Allows a workflow to skip tasks that are not running during the most
recent schedule interval.

If the task is run outside of the latest schedule interval, all
directly downstream tasks will be skipped.

Note that downstream tasks are never skipped if the given DAG_Run is
marked as externally triggered.
Source: https://stackoverflow.com/questions/61252482/difference-between-latest-only-operator-and-catchup-in-airflow

5. LatestOnlyOperator 2 (latest_only_with_triggerschedule)

6. Show kwargs and what is there inside (example_python_operatorschedule)
