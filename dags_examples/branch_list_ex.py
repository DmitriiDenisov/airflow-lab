#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Example DAG demonstrating the usage of BranchPythonOperator with depends_on_past=True, where tasks may be run
or skipped on alternating runs.
"""

from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

args = {
    'owner': 'Airflow',
    'start_date': days_ago(2),
    'depends_on_past': True,
}

# BranchPython operator that depends on past
# and where tasks may run or be skipped on
# alternating runs
dag = DAG(
    dag_id='branch_list_ex',
    schedule_interval=timedelta(minutes=2),
    default_args=args,
    catchup=False,
    tags=['example']
)


def should_run(**kwargs):
    print('------------- exec dttm = {} and minute = {}'.
          format(kwargs['execution_date'], kwargs['execution_date'].minute))
    if kwargs['execution_date'].minute % 3 == 0:
        return ['dummy_task_1', 'dummy_task_3']
    elif kwargs['execution_date'].minute % 6 == 1:
        return ['dummy_task_2', 'dummy_task_4', 'dummy_task_5']
    else:
        return ['dummy_task_6', 'dummy_task_4']


cond = BranchPythonOperator(
    task_id='condition',
    provide_context=True,
    python_callable=should_run,
    dag=dag,
)

dummy_task_1 = DummyOperator(task_id='dummy_task_1', dag=dag)
dummy_task_2 = DummyOperator(task_id='dummy_task_2', dag=dag)
dummy_task_3 = DummyOperator(task_id='dummy_task_3', dag=dag)
dummy_task_4 = DummyOperator(task_id='dummy_task_4', dag=dag)
dummy_task_5 = DummyOperator(task_id='dummy_task_5', dag=dag)
dummy_task_6 = DummyOperator(task_id='dummy_task_6', dag=dag)
cond >> [dummy_task_1, dummy_task_2, dummy_task_3, dummy_task_4, dummy_task_5, dummy_task_6]