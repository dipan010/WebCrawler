from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from processing.processUpload import process_articles

default_args = {
    'start_date': datetime(2025, 5, 1),
    'catchup': False
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

    [process_newsapi_articles, process_crawler_articles]