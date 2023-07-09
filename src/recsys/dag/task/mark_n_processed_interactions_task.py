from .python_rec_sys_operator import python_rec_sys_operator


def python_callable(**ctx):
    import sys
    sys.path.append(ctx['rec_sys_src_path'])
    from recsys.domain_context import DomainContext
    from recsys.util import Picket
    import pandas as pd
    import logging

    domain = DomainContext(cfg_path = ctx['rec_sys_cfg_path'])

    # Only run when found an interactions size change...

    n_interactions = pd.read_json(
        f'{domain.cfg.temp_path}/{ctx["interactions_path"]}',
        orient='records'
    ).shape[0]

    # Save input interactions count...
    Picket.save(
        f'{domain.cfg.temp_path}/check_interactions_change.picket',
        { 'n_interactions': n_interactions }
    )


def mark_n_processed_interactions_task(dag, interactions_path, task_id='mark_n_processed_interactions'):
    return python_rec_sys_operator(
        dag,
        task_id,
        python_callable,
        params = { 'interactions_path': interactions_path}
    )


