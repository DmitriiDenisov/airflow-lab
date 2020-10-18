from airflow.models import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator

args = {
    'owner': 'Airflow',
    'start_date': datetime(2020, 9, 18),
    'depends_on_past': True,
}

temp_command = """
for i in {1..5}
do
   echo "Welcome $i times"
done
"""

dag = DAG(
    dag_id='long_bash',
    schedule_interval=timedelta(minutes=30),
    default_args=args,
    catchup=False,
    tags=['example']
)

hello_my_task = BashOperator(
    task_id='hello_task',
    bash_command=temp_command,
    dag=dag,
)
