from airflow.models import Variable
from airflow.operators.python import ExternalPythonOperator


def python_rec_sys_operator(dag, task_id, python_callable, params={}):
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
        provide_context=True,
        do_xcom_push=True,
        op_kwargs=op_kwargs
    )
