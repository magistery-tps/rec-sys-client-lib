from .python_rec_sys_operator import python_rec_sys_operator
import numpy as np


def python_callable(**ctx):
    import sys
    sys.path.append(ctx['rec_sys_src_path'])
    from recsys.domain_context  import DomainContext
    from recsys.util            import Picket
    import pandas as pd
    import numpy  as np
    from   surprise     import SVD, NMF
    from   scipy        import sparse
    from   recsys.model import SurpriseTrainPredictFn

    domain = DomainContext(cfg_path = ctx['rec_sys_cfg_path'])

    # --------------------------------------------------------------------------
    # Functions
    # --------------------------------------------------------------------------

    def save_interactions(df, name):
        df.to_json(
            f'{domain.cfg.temp_path}/{ctx["task_id"]}_{name}_interactions.json',
            orient='records'
        )


    def load_interactions():
        return pd.read_json(
            f'{domain.cfg.temp_path}/{ctx["interactions_path"]}',
            orient='records'
        )

    # --------------------------------------------------------------------------
    # Main Process
    # --------------------------------------------------------------------------

    train_interactions = load_interactions()

    model = SVD() if ctx['model'].upper() == 'SVD' else NMF()

    # Predict user-item future interactions from train interactions..
    future_interactions, filtered_train_interactions = domain.interaction_inference_service.create(
        train_interactions,
        train_predict_fn   = SurpriseTrainPredictFn(model),
        min_n_interactions = ctx['min_n_interactions'],
        rating_scale       = ctx['rating_scale'],
        columns            = ('user_seq', 'item_seq', 'rating')
    )

    save_interactions(future_interactions, 'future')
    save_interactions(filtered_train_interactions, 'train')




def compute_surprise_rating_matrix_task(
    dag,
    task_id,
    interactions_path,
    model              = 'svd',
    min_n_interactions = 20,
    rating_scale       = np.arange(0, 6, 0.5)
):
    return python_rec_sys_operator(
        dag,
        task_id,
        python_callable,
        params = {
            'interactions_path'  : interactions_path,
            'model'              : model,
            'min_n_interactions' : min_n_interactions,
            'rating_scale'       : rating_scale
        }
    )


