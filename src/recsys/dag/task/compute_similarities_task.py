from .python_rec_sys_operator import python_rec_sys_operator


def python_callable(**ctx):
    import sys
    sys.path.append(ctx['rec_sys_src_path'])
    from recsys.domain_context import DomainContext
    from recsys.util import Picket
    import pandas as pd
    import numpy  as np
    from surprise import SVD, NMF
    from scipy import sparse

    domain = DomainContext(cfg_path = ctx['rec_sys_cfg_path'])

    # --------------------------------------------------------------------------
    # Functions
    # --------------------------------------------------------------------------

    def load_interactions(path):
        return pd.read_json(
            f'{domain.cfg.temp_path}/{ctx[path]}',
            orient='records'
        )

    train_interactions  = load_interactions('train_interactions_path')
    future_interactions = load_interactions('future_interactions_path')
    
    interactions = np.concatenate

    domain.rating_matrix_service.create(
        self,
        train_interactions,
        future_interactions,
        columns=('user_seq', 'item_seq', 'rating'),
        matrix_type=RatingMatrixType.USER_ITEM
    )

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


def compute_similarities_task(
    dag,
    task_id,
    train_interactions_path,
    future_interactions_path
):
    return python_rec_sys_operator(
        dag,
        task_id,
        python_callable,
        params = {
            'train_interactions_path': train_interactions_path,
            'future_interactions_path': future_interactions_path
        }
    )


