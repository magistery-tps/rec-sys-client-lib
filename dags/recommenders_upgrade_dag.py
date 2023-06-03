import sys
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.models import Variable

sys.path.append(Variable.get('recsys.client.src_path'))

import recsys.dag.task as ts
import numpy as np


with DAG(
    'Recommenders-Upgrade',
    default_args       = {
        'owner'           : 'airflow',
        'depends_on_past' : False,
        'email'           : ['adrianmarino@gmail.com'],
        'email_on_failure': False,
        'email_on_retry'  : False,
        'retries'         : 3,
        'retry_delay'     : timedelta(minutes=120)
    },
    description       = """
        This DAG perform next steps: Fetch all user interactions from rec-sys API,
        filter interactions for users with more that 20 interactions.
        Then for each model: train it using user interactions, compute rating matrix
        for all interactions real and predicted. Use rating matrix to compute user-user
        and item-item similarity matrix and upsert matrix to rec-sys API.
        Finally, compute user-user and item-item similarity matrix using mean from
        all model similarity matrix and upsert to rec-sys API.
    """,
    schedule_interval = '*/10 * * * *',
    start_date        = days_ago(0),
    catchup           = False,
    max_active_runs   = 1,
    tags              = ['rec-sys', 'distance-matrix-computing', 'svd', 'nmf']
) as dag:

    fetch = ts.fetch_interactions_task(dag, task_id = 'fetch_interactions')


    check_count = ts.check_interactions_change_task(dag, interactions_path = 'fetch_interactions.json')

    check_branch = ts.branch_task(dag, true_task_id = ['compute_svd_rating_matrix', 'compute_nmf_rating_matrix'])

    mark = ts.mark_n_processed_interactions_task(dag, interactions_path = 'fetch_interactions.json')

    svd_rating_matrix = ts.compute_surprise_rating_matrix_task(
        dag,
        task_id           = 'compute_svd_rating_matrix',
        interactions_path = 'fetch_interactions.json',
        model             = 'SVD',
        min_n_interactions = 20,
        rating_scale       = np.arange(0, 6, 0.5)
    )

    nmf_rating_matrix = ts.compute_surprise_rating_matrix_task(
        dag,
        task_id           = 'compute_nmf_rating_matrix',
        interactions_path = 'fetch_interactions.json',
        model             = 'NMF',
        min_n_interactions = 20,
        rating_scale       = np.arange(0, 6, 0.5)
    )

    svd_sim = ts.compute_similarities_task(
        dag,
        task_id            = 'compute_svd_similarities',
        rating_matrix_path = 'compute_svd_rating_matrix.npz'
    )

    nmf_sim = ts.compute_similarities_task(
        dag,
        task_id            = 'compute_nmf_similarities',
        rating_matrix_path = 'compute_nmf_rating_matrix.npz'
    )

    upgrade_svd_rec = ts.update_recommender_task(
        dag,
        task_id                = 'update_svd_recommender',
        recommender_name       = 'SVD',
        interactions_path      = 'fetch_interactions.json',
        user_similarities_path = 'compute_svd_similarities_user_similarities.json',
        item_similarities_path = 'compute_svd_similarities_item_similarities.json',
        n_most_similars_users  = 50,
        n_most_similars_items  = 10
    )

    upgrade_nmf_rec = ts.update_recommender_task(
        dag,
        task_id                = 'update_nmf_recommender',
        recommender_name       = 'NMF',
        interactions_path      = 'fetch_interactions.json',
        user_similarities_path = 'compute_nmf_similarities_user_similarities.json',
        item_similarities_path = 'compute_nmf_similarities_item_similarities.json',
        n_most_similars_users  = 50,
        n_most_similars_items  = 10
    )

    fetch >> check_count >> check_branch

    check_branch >> svd_rating_matrix >> svd_sim >> upgrade_svd_rec
    check_branch >> nmf_rating_matrix >> nmf_sim >> upgrade_nmf_rec

    [upgrade_svd_rec, upgrade_nmf_rec] >> mark
