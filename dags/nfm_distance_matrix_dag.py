from datetime import timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.utils.dates import days_ago
from dag_utils import BashTaskBuilder


with DAG(
        'NMF-Distance-Matrix-Computing-Job',
        default_args={
                'owner': 'adrian',
                'depends_on_past': False,
                'retries': 5,
                'retry_delay': timedelta(seconds=10),
                'max_active_runs': 1
        },
        description='NMF-Distance-Matrix-Computing-Job',
        schedule_interval='*/5 * * * *',
        start_date=days_ago(0),
        catchup=False,
        tags=['rec-sys']
) as dag:
        # Create all tasks...
        job_task = BashTaskBuilder('nmf_distance_matrix_task') \
                .script('python bin/nmf_distance_matrix_job.py') \
                .build()

        # Workflow...
        job_task
