import json, requests
from datetime import datetime
from airflow.models import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator

translate_url = 'https://api.funtranslations.com/translate/yoda.json'
advice_url = 'https://api.adviceslip.com/advice'
proxies = {'https': 'http://surf-proxy.intranet.db.com:8080/'}

def store_advice(ti) -> None:
    res = requests.get(advice_url, proxy)
    advice = json.loads(res.text)['advice']
    ti.xcom_push(key='advice', value=advice)

def translate_advice(ti) -> None:
    advice = ti.xcom_pull(key='advice')
    #url=translate_url+advice
    res = requests.post(translate_url, data={'text',advice}, proxies=proxies)

with DAG(
    dag_id='fun_api_translation_dag',
    schedule_interval='@daily',
    start_date=datetime(2022, 4, 30),
    catchup=False
) as dag:

    # 1. Check if the advice API is up
    task_is_advice_api_active = HttpSensor(
        task_id='is_advice_api_active',
        http_conn_id='sa_external_advice',
        endpoint='advice'
    )

    # 2. Get the advice
    task_get_advice = PythonOperator(
        task_id='get_advice',
        python_callable=store_advice
    )

    # 3. Check if the translator API is up
    task_is_translator_api_active = HttpSensor(
        task_id='is_translator_api_active',
        http_conn_id='sa_external_translation',
        endpoint='translate'
    )

    # 4. Translate the advice.
    task_translate_advice = PythonOperator(
        task_id='translate_advice',
        python_callable=translate_advice
    )
    

    task_is_advice_api_active>>task_get_advice>>task_is_translator_api_active>>task_translate_advice