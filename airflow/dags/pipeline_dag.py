# Airflow DAG - orchestrates the full pipeline daily
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
}

with DAG(
    dag_id='ecommerce_pipeline',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    kafka_ingest = BashOperator(
        task_id='kafka_consumer',
        bash_command='python /opt/kafka/consumer.py'
    )

    spark_transform = BashOperator(
        task_id='spark_transform',
        bash_command='spark-submit s3://your-bucket/scripts/transform_orders.py'
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='dbt run --project-dir /opt/dbt/ecommerce'
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='dbt test --project-dir /opt/dbt/ecommerce'
    )

    kafka_ingest >> spark_transform >> dbt_run >> dbt_test
