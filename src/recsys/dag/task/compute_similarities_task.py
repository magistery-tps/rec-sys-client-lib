from .python_rec_sys_operator import python_rec_sys_operator


def python_callable(**ctx):
    import sys
    sys.path.append(ctx['rec_sys_src_path'])
    from recsys.domain_context import DomainContext
    import pandas as pd

    domain = DomainContext(cfg_path=ctx['rec_sys_cfg_path'])

    # --------------------------------------------------------------------------
    # Functions
    # --------------------------------------------------------------------------

    def load_interactions(path):
        complete_path = f'{domain.cfg.temp_path}/{ctx[path]}'
        return pd.read_json(complete_path, orient='records')

    def save_similarities(df, name):
        complete_path = f'{domain.cfg.temp_path}/{ctx["task_id"]}_{name}_similarities.json'
        df.to_json(complete_path, orient='records')

    # --------------------------------------------------------------------------
    # Main Process
    # --------------------------------------------------------------------------

    train_interactions = load_interactions('train_interactions_path')
    future_interactions = load_interactions('future_interactions_path')

    rating_matrix = domain.rating_matrix_service.create(
        train_interactions,
        future_interactions,
        columns=('user_seq', 'item_seq', 'rating')
    )
    del train_interactions
    del future_interactions

    #
    # Build similarity matrix from rating matrix...
    #

    user_similarities = domain.similarity_service.similarities(
        rating_matrix,
        entity='user'
    )
    save_similarities(user_similarities, 'user')
    del user_similarities

    item_similarities = domain.similarity_service.similarities(
        rating_matrix.transpose(),
        entity='item'
    )
    del rating_matrix

    save_similarities(item_similarities, 'item')
    del item_similarities


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
        params={
            'train_interactions_path': train_interactions_path,
            'future_interactions_path': future_interactions_path
        }
    )
