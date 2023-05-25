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

    interactions = pd.read_json(
        f'{domain.cfg.temp_path}/{ctx["interactions_path"]}',
        orient='records'
    )

    model = SVD() if ctx['model'].upper() == 'SVD' else NMF()

    # Build ratings matrix from user-item interactions..
    rating_matrix, _ = domain.rating_matrix_service.create(
        interactions,
        columns            =('user_seq', 'item_seq', 'rating'),
        model              = model,
        min_n_interactions = 20,
        rating_scale       = np.arange(0, 6, 0.5)
    )

    ut.Picket.save(
        f'{domain.cfg.temp_path}/{ctx["task_id"]}.picket',
        rating_matrix
    )




def compute_surprise_rating_matrix_task(dag, task_id, interactions_path, model = 'svd'):
    return python_rec_sys_operator(
        dag,
        task_id,
        python_callable,
        params = {'interactions_path': interactions_path, 'model': model }
    )


