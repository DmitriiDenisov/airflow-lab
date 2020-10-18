from airflow.models import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator

args = {
    'owner': 'Airflow',
    'start_date': datetime(2020, 9, 18),
    'depends_on_past': True,
}

dag = DAG(
    dag_id='test_1_new',
    schedule_interval=timedelta(minutes=6),
    default_args=args,
    catchup=False,
    tags=['example']
)

hello_my_task = BashOperator(
    task_id='hello_task',
    bash_command='echo "hello_world"',
    dag=dag,
)
