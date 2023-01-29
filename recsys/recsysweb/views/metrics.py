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

    user_ndcg_timeline_plot, user_ndcg_hist_plot = user_plots(user_ndcg_values)
    all_users_ndgc_timeline_plot, all_user_ndcg_hist_plot = all_users_plots(all_users_ndgc_values)

    response = {
        'user_ndcg'                 : round(user_ndcg, 3) if user_ndcg else None,
        'user_ndcg_timeline'        : user_ndcg_timeline_plot,
        'user_ndcg_hist'            : user_ndcg_hist_plot,

        'all_users_ndgc'            : round(all_users_ndgc, 3) if all_users_ndgc else None,
        'all_users_ndgc_timeline'   : all_users_ndgc_timeline_plot,
        'all_users_ndcg_hist'       : all_user_ndcg_hist_plot
    }

    return render(request, 'single/metrics.html', response)



def user_plots(df):
    if df.empty:
        return None, None
    else:
        df.rename(columns={'value': 'NDCG'}, inplace=True)
        df['Step'] = df.index
        df = df.round({'NDCG': 3})


        timeline_fig = px.line(
            df,
            x='Step',
            y='NDCG',
            markers=True,
            title='Timeline: NDCG by vote step.'
        )
        timeline_fig = plot(timeline_fig, output_type='div')

        hist_fig = px.histogram(
            df,
            x='NDCG',
            nbins=2,
            title='Histogram: Vote steps by NDCG.'
        )
        hist_fig = plot(hist_fig, output_type='div')

        return timeline_fig, hist_fig



def all_users_plots(df):
    if df.empty:
        return None, None
    else:
        df = df \
            .groupby([df['datetime'].dt.hour], as_index=False) \
            .value \
            .mean() \
            .reset_index(names='datetime')

        timeline_fig = px.line(
            df,
            x='datetime',
            y='value',
            markers=True,
            title='Timeline: Mean NDCG by hour.',
            labels={
                'value': 'NDCG',
                'value': 'Hour'
            }
        )
        timeline_fig = plot(timeline_fig, output_type='div')

        hist_fig = px.histogram(
            df,
            x='value',
            nbins=4,
            title='Histogram: Vote steps by NDCG.',
            labels={
                'value': 'NDCG'
            }
        )
        hist_fig = plot(hist_fig, output_type='div')

        return timeline_fig, hist_fig