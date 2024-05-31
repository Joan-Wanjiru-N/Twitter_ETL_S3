from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from Twitter.dags import run_twitter_etl

default_args = {
    'owner' : 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 1),
    'email': ['j.eliton.jn@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'twitter_dag',
    default_args= default_args
    description= 'Pulls data from twitter api to and s3 bucket'
)
run_etl = PythonOperator(
    task_id = 'complete_twitter_etl',
    python_callable= run_twitter_etl,
    dag = dag
)

run_etl