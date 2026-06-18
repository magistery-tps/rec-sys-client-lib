from airflow.models import Variable
from airflow.providers.standard.operators.python import ExternalPythonOperator


def python_rec_sys_operator(dag, task_id, python_callable, params={}, is_gpu=False):
    pool = 'gpu_pool' if is_gpu else 'default_pool'
    op_kwargs = {
        'task_id': task_id,
        'rec_sys_src_path': Variable.get('recsys.client.src_path'),
        'rec_sys_cfg_path': Variable.get('recsys.client.cfg_path'),
        'airflow_path': Variable.get('airflow_path')
    }
    op_kwargs.update(params)

    return ExternalPythonOperator(
        dag=dag,
        python=Variable.get("recsys.client.env_path"),
        task_id=task_id,
        python_callable=python_callable,

        do_xcom_push=True,
        op_kwargs=op_kwargs,
        pool=pool
    )
