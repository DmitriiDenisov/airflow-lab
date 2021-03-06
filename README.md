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
airflow db init

# Create user (just example)
airflow users create -e dmitry@gmail.com -f Dmitry -l Denisov -r Admin -u dmitry -p 123
```

## Start webserver and scheduler:

On my server (bank-bot) two AIrflows are installed, in order to use the correct one use `sudo su` and after it put commands below:

1. `airflow webserver -p 9091 -D` (**Important: if Airflow webserver does not start in daemon (-D) mode then `sudo rm ~/airflow/airflow-webserver-monitor.pid && sudo rm ~/airflow/airflow-webserver.err`**
[Source](https://stackoverflow.com/questions/54737229/airflow-server-is-not-running-in-daemon-mode))
2. `airflow scheduler -D`
(in case if scheduler does not run in Daemon mode try to run `sudo rm  ~/airflow/airflow-scheduler.err  && sudo rm ~/airflow/airflow-scheduler.pid`)
3. Check: go to url <ip>:9091



## Stop Airflow:

1. `cat ~/airflow/airflow-webserver.pid | xargs kill -9` (will take around 30 secs to stop it)
2. (optional) To check that all stopped: `lsof -i tcp:9091`

Source: https://vujade.co/install-apache-airflow-ubuntu-18-04/

## Uninstall Airflow:

`pip3 uninstall apache-airflow `

## Bank-bot part:

Folder `models` and file `my_new_dag.py` are parts of [bank-bot](https://github.com/DmitriiDenisov/bank-bot) project. In order to check it put both of them into `~/airflow/dags` folder


## TroubleShooting:

Config path: `~/airflow/airflow.cfg`

Path to DAGs: `~/airflow/dags$`

If `The secret_key setting under the webserver config has...` then:

1. Generate string `openssl rand -hex 30`

2. Copy generated string into config file for secret_key = generated_string (under flask)

If `ValueError: invalid SameSite value; must be 'Strict', 'Lax' or None` then:

`pip install 'werkzeug<1.0.0'`

if `DataBase is locker`:

Try to run `airflow db init`

## Remove Example Dags from UI:

1. While Airflow is running set `load_examples = False` in `airflow.cfg`

2. `airflow db reset`

[Source](https://stackoverflow.com/questions/43410836/how-to-remove-default-example-dags-in-airflow)

## Hide sensitive variables in UI:

Airflow Variables: Value of a variable will be hidden if the key contains any words in (‘password’, ‘secret’, ‘passwd’, ‘authorization’, ‘api_key’, ‘apikey’, ‘access_token’)

## Tutorials

1. **BashOperator (dag_bash_operator.py / dag_bash_operator_long.py)**

`dag_bash_operator` - example of simple bash operator

`dag_bash_operator_long` - extended previous example where there are multiple rows for Bash Command

*catchup parameter* 

An Airflow DAG with a start_date, possibly an end_date, and a schedule_interval defines a series of intervals which the scheduler turns into individual DAG Runs and executes. The scheduler, by default, will kick off a DAG Run for any interval that has not been run since the last execution date (or has been cleared). This concept is called Catchup.

`catchup=False` means that all previous skipped runs won't run. For example, if you set 'start_date': datetime(2020, 10, 30, 0, 0) and schedule_interval=timedelta(hours=1) and you uploaded your dag at datetime(2020, 10, 30, 3, 30) then it means that 3 runs were skipped and once you uploaded your new DAG it will run initially 3 times, in order to skip it use `catchup=False` parameter

Source: https://airflow.apache.org/docs/stable/dag-run.html#:~:text=DAG%20run%20fails.-,Catchup,individual%20DAG%20Runs%20and%20executes.

2. **PythonOperator and multiple tasks in DAG (python_operator_ex.py)**

This is an example of Python Operator + two connected tasks 

3. **Show parameters of default_args in DAG (default_args_ex.py)**

Possible parameters for default_args for DAG and how to pass params to BashOperator

4. **More complicated structure of DAG: (dag_more_complex.py)**

dagrun_timeout - default value is None. If you set it to some value (for example timedelta(minutes=5)) be aware that if DAG won't finish within 5 minutes then it will be marked as unsuccessful (low perfomance computers/servers might affect)

5. **ShortCircuitOperator - skip downstream tasks based on evaluation of some condition (short_circuit_ex.py)**

Example of how to use ShortCircuitOperator + example of how to use `airflow.utils.helpers.chain` which is alternative way of using `<<`

7. **BranchPythonOperator (3 examples) (branch_operator_ex_1.py, branch_operator_ex_2.py, branch_operator_ex_3.py)**

Sometimes you need a workflow to branch, or only go down a certain path based on an arbitrary condition which is typically related to something that happened in an upstream task. One way to do this is by using the BranchPythonOperator. The BranchPythonOperator is much like the PythonOperator except that it expects a python_callable that returns a task_id (or list of task_ids). The task_id returned is followed, and all of the other paths are skipped. The task_id returned by the Python function has to reference a task directly downstream from the BranchPythonOperator task.

branch_operator_ex_1.py - randomly chooses one of 4

branch_operator_ex_2.py - more complex structure, but alwasy chooses same path 

branch_operator_ex_3.py - depending on some condition it chooses path 

Source1: https://stackoverflow.com/questions/43678408/how-to-create-a-conditional-task-in-airflow

Source2: https://airflow.apache.org/docs/stable/concepts.html?highlight=xcom#branching

8. **BranchPythonOperator - return list of tasks (branch_list_ex.py)**

Same as previous but this time we will return list of task_ids and instead of one path we choose multiple paths 

9. **LatestOnlyOperator (2 examples) (latest_only_with_trigger.py and latest_only_with_trigger_more_complex.py)**

Suppose there is a task t = LatestOnlyOperator (). If the DAG starts before the current date, then instead of skipping all tasks (catchup = False), this operator skips all tasks that depends on the task t, meanwhile all the rest will be run. 

Allows a workflow to skip tasks that are not running during the most
recent schedule interval.

If the task is run outside of the latest schedule interval, all
directly downstream tasks will be skipped.

Note that downstream tasks are never skipped if the given DAG_Run is
marked as externally triggered.

In **latest_only_with_trigger.py** tasks 1, 3 won't be run (as they are downsteams of LatestOnlyOperator) meanwhile tasks 2 and latest_only will be run. Task 4 will aslo run as it has `trigger_rule=TriggerRule.ALL_DONE` [Source](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html#latest-run-only)

In **latest_only_with_trigger_more_complex.py** tasks won't be run 1, 3 meanwhile tasks 2, 5, 6, 7 and latest_only will be run. Task 4 will aslo run as it has `trigger_rule=TriggerRule.ALL_DONE`

Source: https://stackoverflow.com/questions/61252482/difference-between-latest-only-operator-and-catchup-in-airflow

10. **How to pass inside argument + kwards (example_pass_args.py)**

`op_kwargs` shows how to pass inside PythonOperator arguments

Parameter `provide_context=True` allows to pass inside python operator two features: ds and kwargs, in this example they are printed out so you will see them in logs in Airflow. Inside there is only metadata

Explanation for `ds` feature in python function: https://stackoverflow.com/questions/40531952/airflow-pythonoperator-why-to-include-ds-arg 

11. **Trigger another DAG using TriggerDagRunOperator (example_trigger_controller_dag.py** triggers **example_trigger_target_dag.py)**

`Example_trigger_target_dag` is ordinary dag. `Example_trigger_controller_dag` uses `TriggerDagRunOperator` which calls inside python-callable function which decides whether to trigger target dag or not + it passes params inside this python-callable function
**Important: when you trigger controller dag add variable to AirFlow variables: {"should_trigger": true}**

12. **Xcoms (cross communication) (xcom_ex.py)**

XComs let tasks exchange messages, allowing more nuanced forms of control and shared state. The name is an abbreviation of “cross-communication”. XComs are principally defined by a key, value, and timestamp, but also track attributes like the task/DAG that created the XCom and when it should become visible. Any object that can be pickled can be used as an XCom value, so users should make sure to use objects of appropriate size.

XComs can be “pushed” (sent) or “pulled” (received). When a task pushes an XCom, it makes it generally available to other tasks. Tasks can push XComs at any time by calling the xcom_push() method. In addition, if a task returns a value (either from its Operator’s execute() method, or from a PythonOperator’s python_callable function), then an XCom containing that value is automatically pushed.

Tasks call xcom_pull() to retrieve XComs, optionally applying filters based on criteria like key, source task_ids, and source dag_id. By default, xcom_pull() filters for the keys that are automatically given to XComs when they are pushed by being returned from execute functions (as opposed to XComs that are pushed manually).

If xcom_pull is passed a single string for task_ids, then the most recent XCom value from that task is returned; if a list of task_ids is passed, then a corresponding list of XCom values is returned.

13. **Airflow variables + json config (variable_ex.py)**

It shows both: parse of json config and separate variables

[Source](https://www.applydatascience.com/airflow/airflow-variables/)


[Source for all](https://airflow.apache.org/docs/stable/concepts.html?highlight=xcom#branching)
