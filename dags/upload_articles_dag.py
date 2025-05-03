from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from processing.processUpload import process_articles


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
    "upload_article",
    default_args=default_args,
    schedule_intervals = "@daily",
    description="DAG to transform, validate, and upload articles to S3"
) as dag:
    
    process_newsapi_articles = PythonOperator(
        task_id="process_newsapi",
        python_callable=process_articles,
        op_kwargs={
            "filepath": "/app/output/newsapi_output.json", 
            "source": "newsapi"
        },
    )

    process_crawler_articles = PythonOperator(
        task_id="process_crawlers",
        python_callable=process_articles,
        op_kwargs={
            "filepath": "/app/output/crawlers_output.json", 
            "source": "crawler"
        },
    )

    slack_alert = SlackWebhookOperator(
        task_id='slack_failure_alert',
        http_conn_id='slack_connection',
        message=":rotating_light: *DAG upload_articles_pipeline failed!* Check Airflow logs.",
        channel="#alerts",
        trigger_rule="one_failed"
    )

    [process_newsapi_articles, process_crawler_articles] >> slack_alert