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
DAG for dbrun daily
"""

from airflow.models.dag import DAG

from airflow.operators.dummy import DummyOperator
from airflow.sensors.date_time import DateTimeSensor
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.contrib.operators.ssh_operator import SSHOperator

from airflow.utils.dates import days_ago

import datetime

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
    target_time = f"{{{{ {exec_date} }}}}"
    task_id_str = f"wait_till_{hour:02d}{minute:02d}{second:02d}"
    tsk = DateTimeSensor(
        task_id=task_id_str, target_time=target_time, dag=dag, poke_interval=5)
    return tsk


def sh_ssh_hook(node_id, username):
    return SSHHook(
             remote_host=node_id,
             username=username,
             key_file=f'/home/eqops_dev/airflow/keys/ssh.{username}.key')


# [START dbrun_daily]
dag = DAG(
    dag_id="dbrun_daily",
    default_args={
        "depends_on_past": True,
        "retries": 1,
        "retry_delay": datetime.timedelta(minutes=3),
    },
    tags=["dbrun"],
    # start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    start_date=days_ago(2),  # start of the DAG's first data interval
    description="A simple tutorial DAG",
    schedule_interval="@daily",
    catchup=False
)

env = {
    "DATACENTER": "LNPROD02",
    "APPLICATION": "DBDOES",
    "SUB_APPLICATION": "DBRUN"
}

#python = "/home/dbrun/miniconda3/envs/dbrun/bin/python"
#jobs = "/home/dbrun/backend/etl/jobs"
#scripts = "/home/dbrun/backend/dbrun/scripts"
#apps = "/home/dbrun/apps"

python = "/home/eqops_dev/miniconda3/envs/dbrun/bin/python"
jobs = "/home/eqops_dev/backend/etl/jobs"
scripts = "/home/eqops_dev/backend/dbrun/scripts"
apps = "/home/eqops_dev/apps"

dbcertnanny = "/usr/bin/dbcertnanny"

hok_1 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_1 = "LDAP_GROUP_AND_USER_LOADER"
cmd_1 = f"{python} {jobs}/ldap_job.py"

hok_2 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_2 = "GATEKEEPER_DATA_GENERATOR_AND_PUBLISHER"
cmd_2 = f"{python} {jobs}/gk/gatekeeper.py --export"

hok_3 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun_sw')
tid_3 = "DBRUN_SW_PERM_CHECKER_p01"
cmd_3 = f"{scripts}/check_perm_dbrun_sw_user.sh"

hok_4 = sh_ssh_hook('cgaslb01.uk.db.com', 'dbrun_sw')
tid_4 = "DBRUN_SW_PERM_CHECKER_b01"
cmd_4 = f"{scripts}/check_perm_dbrun_sw_user.sh"

hok_5 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_5 = "DBRUN_PERM_CHECKER_p01"
cmd_5 = f"{scripts}/check_perm_dbrun_user.sh"

hok_6 = sh_ssh_hook('cgaslb01.uk.db.com', 'dbrun')
tid_6 = "DBRUN_PERM_CHECKER_b01"
cmd_6 = f"{scripts}/check_perm_dbrun_user.sh"

hok_7 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_7 = "DBIB_NAR_SERVER_INFO_LOADER"
cmd_7 = f"{python} {jobs}/dbib/nar_server_info.py"

hok_8 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_8 = "DBIB_NAR_APP_INFO_LOADER"
cmd_8 = f"{python} {jobs}/dbib/nar_app_info.py"

hok_9 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_9 = "DBIB_NAR_DATABASE_INFO_LOADER"
cmd_9 = f"{python} {jobs}/dbib/nar_database_info.py"

hok_10 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_10 = "DBIB_SNOW_USER_INFO_LOADER"
cmd_10 = f"{python} {jobs}/dbib/snow_user_info.py"

hok_11 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_11 = "AUDIT_TRAIL_DATA_PURGE"
cmd_11 = f"{scripts}/dbRunAuditTrailsPurge.sh"

hok_12 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_12 = "POPULATE_DBRUN_ONBOARD_HIST"
cmd_12 = f"{apps}/dbRUNUtilityScripts/dbRunPopulateOnBoardHist.sh"

hok_13 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_13 = "LDAP_GROUP_AND_USER_LOADER_2"
cmd_13 = f"{python} {jobs}/ldap_job/ldap_job.py"

hok_14 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_14 = "LDAP_GROUP_AND_USER_LOADER_3"
cmd_14 = f"{python} {jobs}/ldap_job/ldap_job.py"

hok_15 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_15 = "LDAP_GROUP_AND_USER_LOADER_4"
cmd_15 = f"{python} {jobs}/ldap_job/ldap_job.py"

hok_18 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_18 = "CYBERARK_UNIX_ACC_DETAILS_LOADER"
cmd_18 = f"{python} {jobs}/cbark/cbark_unix_acc_details.py"

hok_21 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_21 = "DBRUN_PLAYBOOKS_CERTIFICATION"
cmd_21 = f"{scripts}/dbrun_update_playbook_status.sh"

hok_22 = sh_ssh_hook('gmatmd03.uk.db.com', 'dbrun')
tid_22 = "DBIB_NAR_SERVER_ACC_INFO_LOADER"
cmd_22 = f"{python} {jobs}/dbib//nar_svr_acc_info.py"

tsw_1 = wait_till(3, 0, 0, dag)
tsw_2 = wait_till(3, 30, 0, dag)
tsw_3 = wait_till(4, 0, 0, dag)
tsw_4 = tsw_3
tsw_5 = tsw_1
tsw_6 = tsw_1
tsw_7 = tsw_1
tsw_8 = wait_till(3, 5, 0, dag)
tsw_9 = tsw_2
tsw_10 = wait_till(3, 45, 0, dag)
tsw_11 = wait_till(2, 30, 0, dag)
tsw_12 = wait_till(5, 0, 0, dag)
tsw_13 = wait_till(9, 0, 0, dag)
tsw_14 = wait_till(15, 0, 0, dag)
tsw_15 = wait_till(21, 0, 0, dag)

tsw_18 = tsw_12

tsw_21 = tsw_3
tsw_22 = wait_till(3, 15, 0, dag)

start = DummyOperator(task_id='start', dag=dag)
end = DummyOperator(task_id="end", dag=dag)

tsk_1 = SSHOperator(task_id=tid_1, command=cmd_1, ssh_hook=hok_1, dag=dag)
tsk_2 = SSHOperator(task_id=tid_2, command=cmd_2, ssh_hook=hok_2, dag=dag)
tsk_3 = SSHOperator(task_id=tid_3, command=cmd_3, ssh_hook=hok_3, dag=dag)
tsk_4 = SSHOperator(task_id=tid_4, command=cmd_4, ssh_hook=hok_4, dag=dag)
tsk_5 = SSHOperator(task_id=tid_5, command=cmd_5, ssh_hook=hok_5, dag=dag)
tsk_6 = SSHOperator(task_id=tid_6, command=cmd_6, ssh_hook=hok_6, dag=dag)
tsk_7 = SSHOperator(task_id=tid_7, command=cmd_7, ssh_hook=hok_7, dag=dag)
tsk_8 = SSHOperator(task_id=tid_8, command=cmd_8, ssh_hook=hok_8, dag=dag)
tsk_9 = SSHOperator(task_id=tid_9, command=cmd_9, ssh_hook=hok_9, dag=dag)
tsk_10 = SSHOperator(task_id=tid_10, command=cmd_10, ssh_hook=hok_10, dag=dag)
tsk_11 = SSHOperator(task_id=tid_11, command=cmd_11, ssh_hook=hok_11, dag=dag)
tsk_12 = SSHOperator(task_id=tid_12, command=cmd_12, ssh_hook=hok_12, dag=dag)
tsk_13 = SSHOperator(task_id=tid_13, command=cmd_13, ssh_hook=hok_13, dag=dag)
tsk_14 = SSHOperator(task_id=tid_14, command=cmd_14, ssh_hook=hok_14, dag=dag)
tsk_15 = SSHOperator(task_id=tid_15, command=cmd_15, ssh_hook=hok_15, dag=dag)

tsk_18 = SSHOperator(task_id=tid_18, command=cmd_18, ssh_hook=hok_18, dag=dag)

tsk_21 = SSHOperator(task_id=tid_21, command=cmd_21, ssh_hook=hok_21, dag=dag)
tsk_22 = SSHOperator(task_id=tid_22, command=cmd_22, ssh_hook=hok_22, dag=dag)

tsw_1 >> tsk_1
tsw_2 >> tsk_2
tsw_3 >> tsk_3
tsw_4 >> tsk_4
tsw_5 >> tsk_5
tsw_6 >> tsk_6
tsw_7 >> tsk_7
tsw_8 >> tsk_8
tsw_9 >> tsk_9
tsw_10 >> tsk_10
tsw_11 >> tsk_11
tsw_12 >> tsk_12
tsw_13 >> tsk_13
tsw_14 >> tsk_14
tsw_15 >> tsk_15

tsw_18 >> tsk_18

tsw_21 >> tsk_21
tsw_22 >> tsk_22

start >> tsk_1 >> tsk_2 >> end
start >> [tsk_3, tsk_4, tsk_5, tsk_6, tsk_7,
          tsk_8, tsk_9, tsk_10, tsk_11, tsk_12,
          tsk_13, tsk_14, tsk_15,
          tsk_18, tsk_21, tsk_22] >> end

# [END dbrun_daily]

