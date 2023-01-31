import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px
from ..graph import GraphFactory, GraphVisualization
import math
import networkx as nx


class ValidationPlot:
    @staticmethod
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


    @staticmethod
    def all_users_plots(df, user_votes_df):
        if df.empty:
            return None, None, None
        else:
            df = df \
                .groupby([df['datetime'].dt.minute], as_index=False) \
                .value \
                .mean() \
                .reset_index(names='datetime')

            df = df.rename(columns={'datetime': 'Minutes'})


            timeline_fig = px.line(
                df,
                x='Minutes',
                y='value',
                markers=True,
                title='Timeline: Mean NDCG by minute.',
                labels={
                    'value': 'NDCG',
                }
            )
            timeline_fig = plot(timeline_fig, output_type='div')

            hist_fig = px.histogram(
                df,
                x='value',
                nbins=3,
                title='Histogram: Vote steps by NDCG.',
                labels={
                    'value': 'NDCG'
                }
            )
            hist_fig = plot(hist_fig, output_type='div')

            user_votes_df = user_votes_df \
                .rename(columns={'user__username': 'User', 'total': 'Vote Steps'})\
                .sort_values(['Vote Steps'], ascending=False)

            user_votes_fig = go.Figure(
                data=[
                    go.Table(
                        header=dict(
                            values=list(user_votes_df.columns),
                            fill_color='paleturquoise',
                            align='left',
                            font_size=18,
                            height=35
                        ),
                        cells=dict(
                            values=user_votes_df.transpose().values.tolist(),
                            fill_color='lavender',
                            align='left',
                            font_size=18,
                            height=35
                        )
                    )
                ]
            )
            user_votes_fig = plot(user_votes_fig, output_type='div')

            return timeline_fig, hist_fig, user_votes_fig


    @staticmethod
    def plot_user_neighbors(
        user_id,
        user_neighbors_id_sim,
        height    = 600,
        width     = 1296,
        showlabel = True
    ):

        max_sim = max([id_sim[1] for id_sim in user_neighbors_id_sim.items()])

        rows = []
        for idx, id_sim in enumerate(user_neighbors_id_sim.items()):
            norm_sim = round(id_sim[1] / max_sim, 6)

            element  = {'source': 1, 'target': norm_sim, 'length': (1-norm_sim)*50, 'weight': norm_sim }

            rows.append(element)

        graph = GraphFactory.create_weihted_graph(
            pd.DataFrame.from_records(rows),
            edge_attr = ['length', 'weight']
        )

        pos = nx.kamada_kawai_layout(graph, weight='length')


        vis = GraphVisualization(
            graph,
            pos,
            node_text_position='top center',
            node_size=40,
            node_color=int,                   # color vertices based on their IDs
            node_text_font_size={4: 30},
            edge_color={(0, 1): '#ff0000'},
            edge_width={(1, 2): 100}
        )
        fig = vis.create_figure(
            showscale=True,\
            colorbar_title='Similarity Level',
            title=f'Nearest Neighbors Users (k={len(rows)})',
            height    = height,
            width     = width
        )

        return plot(fig, output_type='div')