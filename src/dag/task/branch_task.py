import dag.task as ts
import logging
from dag.util import EnhancedTaskContext, XComHelper
from airflow.operators.python_operator import BranchPythonOperator
from dag.util import XComHelper


def python_callable(ti, **_ctx):
    ctx = EnhancedTaskContext(_ctx)

    logging.info(f'Previous task: {ctx.previous_task_id}')

    value = XComHelper.return_value(ti, task_id=ctx.previous_task_id)
    logging.info(f'Value: {value}')

    next_task_id = ctx['true_task_id'] if value == 'True' else ctx['false_task_id']
    logging.info(f'Continue with: {next_task_id} task...')

    return next_task_id



def branch_task(dag, true_task_id, task_id='branch_decision', false_task_id=[]):
    return BranchPythonOperator(
        dag             = dag,
        task_id         = task_id,
        python_callable = python_callable,
        provide_context = True,
        do_xcom_push    = True,
        op_kwargs       = { 'true_task_id'  : true_task_id, 'false_task_id' : false_task_id}
    )