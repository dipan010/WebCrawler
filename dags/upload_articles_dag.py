from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from processing.processUpload import process_articles
from processing.utils.uploader import upload_raw_file
from apiIntegration.newapi_fetcher import fetch_news
from crawlers.spiders import *
import os

DEFAULT_OUTPUT_DIR = "/app/output"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["dipan.ghosh@hotmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2025, 5, 1),
    "catchup": False
}

with DAG(
    dag_id = "upload_article",
    default_args=default_args,
    schedule_intervals = "@daily",
    description="DAG to transform, validate, and upload articles to S3",
    max_active_runs=1,
    tags=["supplychain-logistics-pipeline"]
) as dag:
    
    # Step 1: Fetch NewsAPI articles
    fetch_newsapi = PythonOperator(
        task_id="fetch_newsapi_articles",
        python_callable= fetch_news,
        op_kwargs={"output_path": os.path.join(DEFAULT_OUTPUT_DIR, "newsapi_output.json")},
    )

    # Step 2: Run all spiders (parallel inside script)
    run_spiders = PythonOperator(
        task_id="run_all_spiders",
        python_callable=run_all_spiders,
        op_kwargs={"output_dir": DEFAULT_OUTPUT_DIR},
    )

    # Step 3: Upload raw output from both sources
    upload_newsapi_raw = PythonOperator(
        task_id="upload_newsapi_raw",
        python_callable=upload_raw_file,
        op_kwargs={
            "filepath": os.path.join(DEFAULT_OUTPUT_DIR, "newsapi_output.json"),
            "source": "newsapi",
        },
    )

    upload_crawlers_raw = PythonOperator(
        task_id="upload_crawlers_raw",
        python_callable=upload_raw_file,
        op_kwargs={
            "filepath": os.path.join(DEFAULT_OUTPUT_DIR, "crawlers_output.json"),
            "source": "crawler",
        },
    )

    # Step 4: Process, transform, validate, and upload
    process_newsapi = PythonOperator(
        task_id="process_newsapi_output",
        python_callable=process_articles,
        op_kwargs={
            "filepath": os.path.join(DEFAULT_OUTPUT_DIR, "newsapi_output.json"),
            "source": "newsapi",
        },
    )

    process_crawlers = PythonOperator(
        task_id="process_crawlers_output",
        python_callable=process_articles,
        op_kwargs={
            "filepath": os.path.join(DEFAULT_OUTPUT_DIR, "crawlers_output.json"),
            "source": "crawler",
        },
    )

    # slack_alert = SlackWebhookOperator(
    #     task_id='slack_failure_alert',
    #     http_conn_id='slack_connection',
    #     message=":rotating_light: *DAG upload_articles_pipeline failed!* Check Airflow logs.",
    #     channel="#alerts",
    #     trigger_rule="one_failed"
    # )

    # DAG Dependencies
    fetch_newsapi >> upload_newsapi_raw >> process_newsapi
    run_spiders >> upload_crawlers_raw >> process_crawlers