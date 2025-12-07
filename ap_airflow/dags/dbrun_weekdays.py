#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   https://urldefense.com/v3/__http://www.apache.org/licenses/LICENSE-2.0__;!!KEc8uF_xo8-al5zF!HL4oAiHZjI-tgHQlhtxzUhbWXdpio_hx4mitOabvgRd6BJsrCz329RKsEz7dQvtm$ 
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Example DAG for FDW Runbook: Classic ZM Run, Task: 75000.
"""

from airflow.models.dag import DAG

from airflow.operators.dummy import DummyOperator
from airflow.sensors.date_time import DateTimeSensor
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.contrib.operators.ssh_operator import SSHOperator

from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup

import datetime
# import pendulum


def wait_till(hour: int, minute: int, second: int, dag):
    """
    get a DateTimeSensor runs till hour: minute: second for default timezone

    Parameters
    ----------
    hour : int
        hour in the day
    minute : int
        minute
    second : int
        second
    dag : [type]
        dag
    """
    exec_date = f'next_execution_date.in_tz("Europe/Berlin").replace(hour={hour}, minute={minute}, second={second})'
    target_time = f'{{{{ {exec_date} }}}}'
    task_id_str = f"wait_till_{hour:02d}{minute:02d}{second:02d}"
    tsk = DateTimeSensor(
        task_id=task_id_str, target_time=target_time, dag=dag, poke_interval=5)
    return tsk


def sh_ssh_hook(node_id, username):
    return SSHHook(
             remote_host=node_id,
             username=username,
             key_file=f'/home/eqops_dev/airflow/keys/ssh.{username}.key')


# [START dbrun_weekdays]
dag = DAG(
    dag_id="dbrun_weekdays",
    default_args={
        "depends_on_past": True,
        "retries": 1,
        "retry_delay": datetime.timedelta(minutes=3),
    },
    tags=["dbrun"],
    # start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    start_date=days_ago(2),  # start of the DAG's first data interval
    description="A simple tutorial DAG",
    schedule_interval="0 5 * * 4",
    catchup=False
)

env = {
    "DATACENTER": "LNPROD02",
    "APPLICATION": "DBDOES",
    "SUB_APPLICATION": "DBRUN"
}

start = DummyOperator(task_id="start", dag=dag)
end = DummyOperator(task_id='end', dag=dag)

dbcertnanny = "/usr/bin/dbcertnanny"
cfg = "/usr/bin/dbcertnanny"

hok_16 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_16 = "DBRUN_CERTNANNY_CERT_CHECKER_p01"
cmd_16 = f"{dbcertnanny} --cfg {cfg}/dbcertnanny.cfg manage"

hok_17 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_17 = "DBRUN_CERTNANNY_CERT_CHECKER_b01"
cmd_17 = f"{dbcertnanny} --cfg {cfg}/dbcertnanny.cfg manage"

tsw_16 = wait_till(5, 0, 0, dag)
tsw_17 = tsw_16

tsk_16 = SSHOperator(task_id=tid_16, command=cmd_16, ssh_hook=hok_16, dag=dag)
tsk_17 = SSHOperator(task_id=tid_17, command=cmd_17, ssh_hook=hok_17, dag=dag)

tsw_16 >> tsk_16
tsw_17 >> tsk_17

start >> [tsk_16, tsk_17] >> end

# [END dbrun_weekdays]

