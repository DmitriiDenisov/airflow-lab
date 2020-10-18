from builtins import range
from datetime import timedelta

from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'Airflow',
    'start_date': days_ago(1),
    'depends_on_past': False
}

dag = DAG(
    dag_id='test_5',
    catchup=False,
    default_args=args,
    schedule_interval=timedelta(minutes=3),
    dagrun_timeout=timedelta(minutes=12),
    tags=['example']
)

run_this_last = DummyOperator(
    task_id='run_this_last',
    depends_on_past=False,
    dag=dag,
)

# [START howto_operator_bash]
run_this = BashOperator(
    task_id='run_after_loop',
    depends_on_past=False,
    bash_command='echo 1',
    dag=dag,
)
# [END howto_operator_bash]

run_this >> run_this_last

for i in range(3):
    task = BashOperator(
        task_id='runme_' + str(i),
        bash_command='echo "{{ task_instance_key_str }}" && sleep 1',
        depends_on_past=False,
        dag=dag,
    )
    task >> run_this

# [START howto_operator_bash_template]
also_run_this = BashOperator(
    task_id='also_run_this',
    depends_on_past=False,
    bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"',
    dag=dag,
)
# [END howto_operator_bash_template]
also_run_this >> run_this_last