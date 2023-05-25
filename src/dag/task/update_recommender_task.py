from .python_rec_sys_operator import python_rec_sys_operator


def python_callable(**ctx):
    import sys
    sys.path.append(ctx['src_path'])
    from domain_context import DomainContext
    import util   as ut
    import data   as dt
    import pandas as pd
    import numpy  as np
    from surprise import SVD, NMF
    import logging

    domain = DomainContext(cfg_path = ctx['cfg_path'])


    interactions = pd.read_json(
        f'{domain.cfg.temp_path}/{ctx["interactions_path"]}',
        orient='records'
    )
    user_similarities = pd.read_json(
        f'{domain.cfg.temp_path}/{ctx["user_similarities_path"]}',
        orient='records'
    )
    item_similarities = pd.read_json(
        f'{domain.cfg.temp_path}/{ctx["item_similarities_path"]}',
        orient='records'
    )


    # Update user/item similarity matrix into RecSys API...
    user_similarity_matrix = domain.similarity_matrix_service.update_user_similarity_matrix(
        user_similarities,
        interactions,
        name=f'{ctx["recommender_name"]}-user-to-user',
        n_most_similars=ctx['n_most_similars_users']
    )


    item_similarity_matrix = domain.similarity_matrix_service.update_item_similarity_matrix(
        item_similarities,
        interactions,
        name=f'{ctx["recommender_name"]}-item-to-item',
        n_most_similars=ctx['n_most_similars_items']
    )

    # Create or update recommender and asociate with las verison of user/item
    # similarity matrix into RecSys API...
    domain.recommender_service.upsert(
        ctx["recommender_name"],
        user_similarity_matrix,
        item_similarity_matrix
    )




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
        params = {
            'recommender_name'       : recommender_name,
            'interactions_path'      : interactions_path,
            'user_similarities_path' : user_similarities_path,
            'item_similarities_path' : item_similarities_path,
            'n_most_similars_users'  : n_most_similars_users,
            'n_most_similars_items'  : n_most_similars_items
        }
    )


