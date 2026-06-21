from .python_rec_sys_operator import python_rec_sys_operator


def python_callable(
    task_id,
    rec_sys_src_path,
    rec_sys_cfg_path,
    airflow_path,
    interactions_path
):
    import sys
    sys.path.append(rec_sys_src_path)
    from recsys.domain_context import DomainContext
    from recsys.util import Picket
    import pandas as pd
    from os.path import exists
    import logging

    domain = DomainContext(cfg_path=rec_sys_cfg_path)

    # Only run when found an interactions size change...

    change_mark_path = f'{domain.cfg.temp_path}/check_interactions_change.picket'

    if not exists(change_mark_path):
        logging.info(
            f"\n================================================================================\n"
            f"🚀 FIRST PIPELINE RUN / CLEAN SLATE DETECTED\n"
            f"================================================================================\n"
            f"No previous execution mark was found. Airflow will perform a full retraining run\n"
            f"to initialize the trained models and similarity matrices in the database.\n"
            f"================================================================================\n"
        )
        return 'True'

    n_current_interactions = pd.read_json(
        f'{domain.cfg.temp_path}/{interactions_path}',
        orient='records'
    ).shape[0]

    n_previous_interactions = Picket.load(change_mark_path)['n_interactions']

    if n_current_interactions == n_previous_interactions:
        logging.info(
            f"\n================================================================================\n"
            f"ℹ️ PIPELINE EXECUTION NOTICE (EXPLANATORY DIALOGUE)\n"
            f"================================================================================\n"
            f"The recommendation engine models WILL NOT be re-trained during this run.\n\n"
            f"REASON FOR EXITING EARLY:\n"
            f"The total number of user ratings (interactions) in the system remains unchanged:\n"
            f"  • Current ratings count:  {n_current_interactions}\n"
            f"  • Previous ratings count: {n_previous_interactions}\n\n"
            f"HOW IT WORKS:\n"
            f"The Airflow pipeline is designed to save CPU and server memory by avoiding unnecessary\n"
            f"computation. Since no new ratings have been submitted by any user since the last run,\n"
            f"the existing trained models and collaborative filtering similarity matrices are still\n"
            f"perfectly up-to-date.\n\n"
            f"To trigger a full re-training cycle, please submit at least one new rating/star\n"
            f"interaction on any movie from the Chatbot Web UI.\n"
            f"================================================================================\n"
        )
        return 'False'

    logging.info(
        f"\n================================================================================\n"
        f"🚀 PIPELINE RETRAINING TRIGGERED (EXPLANATORY DIALOGUE)\n"
        f"================================================================================\n"
        f"The recommendation engine models WILL be re-trained during this run!\n\n"
        f"REASON FOR CONTINUING:\n"
        f"A change in the number of user ratings (interactions) has been detected:\n"
        f"  • Current ratings count:  {n_current_interactions}\n"
        f"  • Previous ratings count: {n_previous_interactions}\n\n"
        f"HOW IT WORKS:\n"
        f"New user ratings have been submitted, meaning the collaborative filtering profiles\n"
        f"need to be updated. Airflow will now run the SVD, NMF, GMF, DeepFM, and Nearest\n"
        f"Neighbors algorithms to update the movie-similarity indices for warm-started users.\n"
        f"================================================================================\n"
    )
    return 'True'


def check_interactions_change_task(dag, interactions_path, task_id='check_interactions_change'):
    return python_rec_sys_operator(
        dag,
        task_id,
        python_callable,
        params={'interactions_path': interactions_path}
    )
