# -*- coding: utf-8 -*-
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
Example LatestOnlyOperator and TriggerRule interactions
"""

# [START example]
import datetime as dt

from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.latest_only_operator import LatestOnlyOperator
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule

dag = DAG(
    dag_id='latest_only_ex',
    schedule_interval=dt.timedelta(hours=4),
    start_date=days_ago(2),
    tags=['example']
)

latest_only = LatestOnlyOperator(task_id='latest_only', dag=dag)
task1 = DummyOperator(task_id='task1', dag=dag)
task2 = DummyOperator(task_id='task2', dag=dag)
task3 = DummyOperator(task_id='task3', dag=dag)
task4 = DummyOperator(task_id='task4', dag=dag, trigger_rule=TriggerRule.ALL_DONE)
task5 = DummyOperator(task_id='task5', dag=dag)
task6 = DummyOperator(task_id='task6', dag=dag)
task7 = DummyOperator(task_id='task7', dag=dag)

latest_only >> task1 >> [task3, task4]
task2 >> [task3, task4]
task5 >> task4
task6 >> latest_only
task7 >> task1
# [END example]
