import numpy as np

from .python_rec_sys_operator import python_rec_sys_operator


def python_callable(
    task_id,
    rec_sys_src_path,
    rec_sys_cfg_path,
    airflow_path,
    interactions_path,
    model,
    min_n_interactions,
    rating_scale
):
    import sys
    sys.path.append(rec_sys_src_path)
    from recsys.domain_context import DomainContext
    import pandas as pd
    from surprise import SVD, NMF
    from recsys.model import SurpriseTrainPredictFn

    domain = DomainContext(cfg_path=rec_sys_cfg_path)

    # --------------------------------------------------------------------------
    # Functions
    # --------------------------------------------------------------------------

    def save_interactions(df, name):
        df.to_json(
            f'{domain.cfg.temp_path}/{task_id}_{name}_interactions.json',
            orient='records'
        )

    def load_interactions():
        return pd.read_json(
            f'{domain.cfg.temp_path}/{interactions_path}',
            orient='records'
        )

    # --------------------------------------------------------------------------
    # Main Process
    # --------------------------------------------------------------------------

    interactions = load_interactions()

    model_instance = SVD() if model.upper() == 'SVD' else NMF()

    # Predict user-item future interactions from train interactions..
    future_interactions, filtered_train_interactions = domain.interaction_inference_service.predict(
        interactions,
        columns=('user_seq', 'item_seq', 'rating'),
        train_predict_fn=SurpriseTrainPredictFn(model_instance),
        min_n_interactions=min_n_interactions,
        rating_scale=rating_scale
    )
    del interactions
    del model_instance

    save_interactions(future_interactions, 'future')
    del future_interactions

    save_interactions(filtered_train_interactions, 'train')
    del filtered_train_interactions


def compute_surprise_rating_matrix_task(
        dag,
        task_id,
        interactions_path,
        model='svd',
        min_n_interactions=20,
        rating_scale=np.arange(0, 6, 0.5)
):
    return python_rec_sys_operator(
        dag,
        task_id,
        python_callable,
        params={
            'interactions_path': interactions_path,
            'model': model,
            'min_n_interactions': min_n_interactions,
            'rating_scale': rating_scale
        }
    )
