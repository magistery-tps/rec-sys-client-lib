from .python_rec_sys_operator import python_rec_sys_operator


def python_callable(**ctx):
    import sys
    sys.path.append(ctx['src_path'])
    from domain_context import DomainContext
    import util   as ut
    import pandas as pd
    import numpy  as np
    from surprise import SVD, NMF

    domain = DomainContext(cfg_path = ctx['cfg_path'])

    rating_matrix = ut.Picket.load(f'{domain.cfg.temp_path}/{ctx["rating_matrix_path"]}')

    # Build similarity matrix from rating matrix...
    user_similarities = domain.similarity_service.similarities(
        rating_matrix,
        entity='user'
    )
    user_similarities.to_json(
        f'{domain.cfg.temp_path}/{ctx["task_id"]}_user_similarities.json',
        orient='records'
    )


    item_similarities = domain.similarity_service.similarities(
        rating_matrix.transpose(),
        entity='item'
    )
    item_similarities.to_json(
        f'{domain.cfg.temp_path}/{ctx["task_id"]}_item_similarities.json',
        orient='records'
    )


def compute_similarities_task(dag, task_id, rating_matrix_path):
    return python_rec_sys_operator(
        dag,
        task_id,
        python_callable,
        params = {'rating_matrix_path': rating_matrix_path }
    )


