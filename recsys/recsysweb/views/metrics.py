from django.shortcuts import render
from django.contrib.auth.decorators import login_required



# Domain
from ..models       import Item, RecommenderType
from ..forms        import ItemForm, InteractionForm
from ..domain       import DomainContext
from ..recommender  import RecommenderContext, RecommenderCapability
from ..plot         import ValidationPlot

ctx = DomainContext()


@login_required
def show_metrics(request):
    user_ndcg        = ctx.evaluation_service.find_metric_by_active_and_user(request.user)
    user_ndcg_values = ctx.evaluation_service.find_metric_values_by_active_and_user(request.user)

    all_users_ndgc        = ctx.evaluation_service.find_metric_by_active()
    all_users_ndgc_values = ctx.evaluation_service.find_metric_values_by_active()
    user_votes_df         = ctx.evaluation_service.user_votes_by_active()


    recommender = ctx.recommender_service.find_recommender_from_active_evaluation(request.user)

    recommender_config = recommender.current_config(request.user)


    if recommender_config.type == RecommenderType.COLLAVORATIVE_FILTERING:
        k_neighbors = 20
        element_id_sim_list = ctx.similarity_matrix_service.find_similar_element_ids(
            matrix     = recommender_config.user_similarity_matrix,
            element_id = request.user.id,
            limit      = k_neighbors
        )
        if element_id_sim_list:
            user_neighbors_graph_plot = ValidationPlot.plot_user_neighbors(request.user.id, element_id_sim_list)
        else:
            user_neighbors_graph_plot = None
    else:
        user_neighbors_graph_plot = None

    user_ndcg_timeline_plot, user_ndcg_hist_plot = ValidationPlot.user_plots(user_ndcg_values)

    all_users_ndgc_timeline_plot, all_user_ndcg_hist_plot, user_votes_plot = ValidationPlot.all_users_plots(
        all_users_ndgc_values,
        user_votes_df
    )

    response = {
        'user_ndcg'                 : round(user_ndcg, 3) if user_ndcg else None,
        'user_ndcg_timeline'        : user_ndcg_timeline_plot,
        'user_ndcg_hist'            : user_ndcg_hist_plot,
        'user_neighbors'            : user_neighbors_graph_plot,

        'all_users_ndgc'            : round(all_users_ndgc, 3) if all_users_ndgc else None,
        'all_users_ndgc_timeline'   : all_users_ndgc_timeline_plot,
        'all_users_ndcg_hist'       : all_user_ndcg_hist_plot,
        'user_n_interactions'       : ctx.interaction_service.count_by_user(request.user),

        'user_votes_table'          : user_votes_plot
    }

    return render(request, 'single/metrics.html', response)
