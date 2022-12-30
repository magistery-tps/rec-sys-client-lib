from datetime import timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.utils.dates import days_ago
from dag_utils import BashTaskBuilder


with DAG(
        'multi-qa-mpnet-base-dot-v1-bert-item-distance-matrix',
        default_args={
                'owner': 'adrian',
                'depends_on_past': False,
                'retries': 5,
                'retry_delay': timedelta(seconds=10),
                'max_active_runs': 1
        },
        description='multi-qa-mpnet-base-dot-v1-bert-item-distance-matrix',
        schedule_interval='*/10 * * * *',
        start_date=days_ago(0),
        catchup=False,
        tags=['rec-sys']
) as dag:
        # Create all tasks...
        job_task = BashTaskBuilder('multi-qa-mpnet-base-dot-v1-bert-item-distance-matrix-task') \
                .script('python bin/multi_qa_mpnet_base_dot_v1_bert_item_distance_matrix_job.py') \
                .build()

        # Workflow...
        job_task
