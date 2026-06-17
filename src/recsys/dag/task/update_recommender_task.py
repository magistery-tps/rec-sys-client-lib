from .python_rec_sys_operator import python_rec_sys_operator


def python_callable(
    task_id,
    rec_sys_src_path,
    rec_sys_cfg_path,
    airflow_path,
    recommender_name,
    interactions_path,
    user_similarities_path,
    item_similarities_path,
    n_most_similars_users,
    n_most_similars_items
):
    import sys
    sys.path.append(rec_sys_src_path)
    from recsys.domain_context import DomainContext
    import pandas as pd
    import logging

    domain = DomainContext(cfg_path=rec_sys_cfg_path)

    # --------------------------------------------------------------------------
    # Functions
    # --------------------------------------------------------------------------

    def load_df(path):
        complete_path = f'{domain.cfg.temp_path}/{path}'
        logging.info(f'Load: {complete_path}')
        return pd.read_json(complete_path, orient='records')

    # --------------------------------------------------------------------------
    # Main Process
    # --------------------------------------------------------------------------

    train_interactions = load_df(interactions_path)
    user_similarities = load_df(user_similarities_path)
    item_similarities = load_df(item_similarities_path)

    # Update user/item similarity matrix into RecSys API...
    user_similarity_matrix = domain.similarity_matrix_service.update_user_similarity_matrix(
        user_similarities,
        train_interactions,
        name=f'{recommender_name}-user-to-user',
        n_most_similars=n_most_similars_users
    )
    del user_similarities

    item_similarity_matrix = domain.similarity_matrix_service.update_item_similarity_matrix(
        item_similarities,
        train_interactions,
        name=f'{recommender_name}-item-to-item',
        n_most_similars=n_most_similars_items
    )
    del item_similarities
    del train_interactions

    # Create or update recommender and asociate with las verison of user/item
    # similarity matrix into RecSys API...
    domain.recommender_service.upsert(
        recommender_name,
        user_similarity_matrix,
        item_similarity_matrix
    )
    del user_similarity_matrix
    del item_similarity_matrix


def update_recommender_task(
        dag,
        task_id,
        recommender_name,
        interactions_path,
        user_similarities_path,
        item_similarities_path,
        n_most_similars_users=50,
        n_most_similars_items=10
):
    return python_rec_sys_operator(
        dag,
        task_id,
        python_callable,
        params={
            'recommender_name': recommender_name,
            'interactions_path': interactions_path,
            'user_similarities_path': user_similarities_path,
            'item_similarities_path': item_similarities_path,
            'n_most_similars_users': n_most_similars_users,
            'n_most_similars_items': n_most_similars_items
        }
    )
