import airflow.utils.helpers
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import ShortCircuitOperator

args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

dag = DAG(dag_id='example_short_circuit_operator', default_args=args, tags=['example'])

cond_true = ShortCircuitOperator(
    task_id='condition_is_True',
    python_callable=lambda: True,
    dag=dag,
)

cond_false = ShortCircuitOperator(
    task_id='condition_is_False',
    python_callable=lambda: False,
    dag=dag,
)

ds_true = [DummyOperator(task_id='true_' + str(i), dag=dag) for i in [1, 2]]
ds_false = [DummyOperator(task_id='false_' + str(i), dag=dag) for i in [1, 2]]

airflow.utils.helpers.chain(cond_true, *ds_true)
airflow.utils.helpers.chain(cond_false, *ds_false)