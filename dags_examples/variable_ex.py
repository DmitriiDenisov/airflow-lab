import os
import datetime as dt

import requests
import pandas as pd
from airflow.models import DAG, Variable
from airflow.operators.python_operator import PythonOperator
import datetime

args = {
    'owner': 'Airflow',
    'start_date': dt.datetime(2020, 9, 18),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
    'depends_on_past': False,
}

# Config variables

## 3 DB connections called
var1 = Variable.get("var1")
var2 = Variable.get("var2")
var3 = Variable.get("var3")

## Recommended way
dag_config = Variable.get("example_variables_config", deserialize_json=True)


def first_task():
    print('var1:', var1)
    print('var2:', var2)
    print('var3:', var3)
    return True


def second_task():
    var1 = dag_config["var1"]
    var2 = dag_config["var2"]
    var3 = dag_config["var3"]
    print('dag_config:', dag_config)
    print(type(var1))
    print(type(var2))
    print(type(var3))
    return True


with DAG(dag_id='variable_ex', default_args=args, schedule_interval=dt.timedelta(minutes=7), catchup=False) as dag:
    first_task = PythonOperator(
        task_id='task_1',
        python_callable=first_task,
        dag=dag
    )
    second_task = PythonOperator(
        task_id='task_2',
        python_callable=second_task,
        dag=dag
    )
    first_task >> second_task
