from .python_rec_sys_operator import python_rec_sys_operator


def python_callable(**ctx):
    import sys
    sys.path.append(ctx['src_path'])
    from domain_context import DomainContext
    import util   as ut
    import pandas as pd
    from os.path import exists
    import logging

    domain = DomainContext(cfg_path = ctx['cfg_path'])

    # Only run when found an interactions size change...

    change_mark_path = f'{domain.cfg.temp_path}/check_interactions_change.picket'

    if exists(change_mark_path):
        n_current_interactions = pd.read_json(
            f'{domain.cfg.temp_path}/{ctx["interactions_path"]}',
            orient='records'
        ).shape[0]

        n_previous_interactions = ut.Picket.load(change_mark_path)['n_interactions']
        logging.info(f'n_current_interactions: {n_current_interactions}')
        logging.info(f'n_previous_interactions: {n_previous_interactions}')

        if n_current_interactions == n_previous_interactions:
            logging.info(f'Not found interaction size change.')
            return 'False'


    logging.info(f'Found interaction size change.')
    return 'True'


def check_interactions_change_task(dag, interactions_path, task_id='check_interactions_change'):
    return python_rec_sys_operator(
        dag,
        task_id,
        python_callable,
        params = { 'interactions_path': interactions_path}
    )


