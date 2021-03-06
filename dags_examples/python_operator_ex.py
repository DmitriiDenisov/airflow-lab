import os
import datetime as dt

import requests
import pandas as pd
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
import datetime

args = {
    'owner': 'Airflow',
    'start_date': dt.datetime(2020, 9, 18),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
    'depends_on_past': False,
}

FILENAME = os.path.join(os.path.expanduser('~'), 'titanic.csv')


def download_titanic_dataset():
    url = 'https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv'
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(FILENAME, 'w', encoding='utf-8') as f:
        for chunk in response.iter_lines():
            f.write('{}\\n'.format(chunk.decode('utf-8')))


def pivot_dataset():
    titanic_df = pd.read_csv(FILENAME)
    pvt = titanic_df.pivot_table(
        index=['Sex'], columns=['Pclass'], values='Name', aggfunc='count'
    )
    df = pvt.reset_index()
    df.to_csv(os.path.join(os.path.expanduser('~'), 'titanic_pivot.csv'))


with DAG(dag_id='try_utc', default_args=args, schedule_interval=dt.timedelta(minutes=5),  catchup=False) as dag:
    create_titanic_dataset = PythonOperator(
        task_id='task_1',
        python_callable=download_titanic_dataset,
        dag=dag
    )
    pivot_titanic_dataset = PythonOperator(
        task_id='task_2',
        python_callable=pivot_dataset,
        dag=dag
    )
    create_titanic_dataset >> pivot_titanic_dataset
