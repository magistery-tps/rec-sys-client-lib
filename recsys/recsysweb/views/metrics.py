from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import logging
import pandas as pd


# Domain
from ..models       import Item
from ..forms        import ItemForm, InteractionForm
from ..domain       import DomainContext
from ..recommender  import RecommenderContext, RecommenderCapability


from plotly.offline import plot
import plotly.express as px

ctx = DomainContext()


@login_required
def show_metrics(request):

    user_ndcg        = ctx.evaluation_service.find_metric_by_active_and_user(request.user)
    user_ndcg_values = ctx.evaluation_service.find_metric_values_by_active_and_user(request.user)

    all_users_ndgc        = ctx.evaluation_service.find_metric_by_active()
    all_users_ndgc_values = ctx.evaluation_service.find_metric_values_by_active()

    user_ndcg_values.rename(columns={'value': 'NDCG'}, inplace=True)
    user_ndcg_values['Step'] = user_ndcg_values.index
    user_ndcg_values = user_ndcg_values.round({'NDCG': 3})

    user_ndcg_timeline_fig = px.line(
        user_ndcg_values,
        x='Step',
        y='NDCG',
        markers=True,
        title='Timeline: NDCG by vote step.'
    )

    user_ndcg_hist_fig = px.histogram(
        user_ndcg_values,
        x='NDCG',
        nbins=2,
        title='Histogram: Vote steps by NDCG.'
    )


    all_users_ndgc_values_by_datetime = all_users_ndgc_values \
        .groupby([all_users_ndgc_values['datetime'].dt.hour], as_index=False) \
        .value \
        .mean() \
        .reset_index(names='datetime')


    all_users_ndgc_timeline_fig = px.line(
        all_users_ndgc_values_by_datetime,
        x='datetime',
        y='value',
        markers=True,
        title='Timeline: Mean NDCG by hour.',
        labels={
            'value': 'NDCG',
            'value': 'Hour'
        }
    )

    all_user_ndcg_hist_fig = px.histogram(
        all_users_ndgc_values,
        x='value',
        nbins=4,
        title='Histogram: Vote steps by NDCG.',
        labels={
            'value': 'NDCG'
        }
    )

    response = {
        'user_ndcg'                 : round(user_ndcg, 3),
        'user_ndcg_timeline'        : plot(user_ndcg_timeline_fig, output_type='div'),
        'user_ndcg_hist'            : plot(user_ndcg_hist_fig, output_type='div'),

        'all_users_ndgc'            : round(all_users_ndgc, 3),
        'all_users_ndgc_timeline'   : plot(all_users_ndgc_timeline_fig, output_type='div'),
        'all_users_ndcg_hist'       : plot(all_user_ndcg_hist_fig, output_type='div')
    }

    return render(request, 'single/metrics.html', response)

