from .python_rec_sys_operator import python_rec_sys_operator


def python_callable(**ctx):
    import sys
    sys.path.append(ctx['rec_sys_src_path'])
    from recsys.domain_context import DomainContext
    from recsys.data import Sequencer

    domain = DomainContext(cfg_path=ctx['rec_sys_cfg_path'])

    interactions = domain \
        .interaction_service \
        .find_by(ctx['query'], ctx['page_size'])

    output_path = f'{domain.cfg.temp_path}/{ctx["task_id"]}.json'

    # Add user/item numeric sequences...
    interactions = Sequencer(column='user_id', seq_col_name='user_seq').perform(interactions)
    interactions = Sequencer(column='item_id', seq_col_name='item_seq').perform(interactions)

    interactions.to_json(output_path, orient='records')

    return output_path


def fetch_interactions_task(
        dag,
        task_id,
        query={},
        page_size=5_000
):
    return python_rec_sys_operator(
        dag,
        task_id=task_id,
        python_callable=python_callable,
        params={'query': query, 'page_size': page_size}
    )
