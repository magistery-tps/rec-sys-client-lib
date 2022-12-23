import numpy as np
import api
from repository import InteractionRepository
import util as ut
import seaborn as sns
import multiprocessing as mp
import pandas as pd
from logger import get_logger


class InteractionService:
    def __init__(self, repository: InteractionRepository):
        self.repository = repository
        self._logger    = get_logger(self)


    def seq_by_id(self, df, entity=None, column_id=None, column_seq=None):
        if entity:
            column_id  = f'{entity}_id'
            column_seq = f'{entity}_seq'

        return pd.Series(df[column_id].values, index=df[column_seq]).to_dict()


    def n_interactions_by_user(
        self,
        df,
        columns            = ('user_seq', 'item_seq', 'rating'),
        min_n_interactions = 20
    ):
        return df  \
            .groupby(columns[0], as_index=False)[columns[1]] \
            .count() \
            .rename(columns={columns[1]: 'n_interactions'}) \
            .query('n_interactions >= 20')


    def filter_by_rating_scale(
        self,
        df,
        columns      = ('user_seq', 'item_seq', 'rating'),
        rating_scale = [1, 2, 3, 4, 5]
    ):
        self._logger.info(f'Filter by {columns[2]} scale: {rating_scale}')

        df_filtered = df.pipe(lambda df: df[df[columns[2]].isin(rating_scale)])

        self._logger.info(f'Filtered: {(1- (df_filtered.shape[0] / df.shape[0])) * 100:.1f}%')
        return df_filtered


    def filter_users_by_min_interactions(
        self,
        df,
        columns            = ('user_seq', 'item_seq', 'rating'),
        min_n_interactions = 20,
    ):
        self._logger.info(f'Filter interactions by user_n_interactions >= {min_n_interactions}')

        user_ids = self.n_interactions_by_user(df, columns, min_n_interactions)[columns[0]].unique()
        df_filtered = df[df[columns[0]].isin(user_ids)]

        self._logger.info(f'Filtered interactions: {(1 - (df_filtered.shape[0] / df.shape[0])) * 100:.1f}%')
        self._logger.info(f'Excluded interactions: {df.shape[0] - df_filtered.shape[0]}')

        return df_filtered


    def find_all(self, page_size = 50000):
        return pd.DataFrame.from_records(self.repository.find(page_size=page_size))


    def unrated_user_item(
        self,
        df,
        columns    = ('user_seq', 'item_seq', 'rating'),
        min_rating = 1
    ):
        items_by_user = self.items_by_user(df, columns, min_rating)

        all_item_ids = set(df[columns[1]].unique())

        data = []
        for user_id, rated_item_ids in items_by_user.items():
            for unrated_item_id in (all_item_ids - rated_item_ids):
                data.append({columns[0]: user_id, columns[1]: unrated_item_id})

        unrated_interactions = pd.DataFrame(data)

        total = df[columns[0]].unique().shape[0] * df[columns[1]].unique().shape[0]
        percent = (unrated_interactions.shape[0] / total) * 100
        self._logger.info(f'Unrated interactions: {percent:.1f}%')

        return unrated_interactions


    def items_by_user(
        self,
        df,
        columns    = ('user_seq', 'item_seq', 'rating'),
        min_rating = 1
    ):
        items_by_user = {}

        for _, row in df.iterrows():
            if row[columns[2]] == None or row[columns[2]] < min_rating:
                continue

            user_id, item_id = row[columns[0]].astype(int), row[columns[1]].astype(int)

            if user_id not in items_by_user:
                items_by_user[user_id] = set()

            items_by_user[user_id].add(item_id)

        return items_by_user


    def plot_n_users_by_item(self, df, columns = ('user_id', 'item_id', 'rating')):
        item_users = df \
            .groupby(columns[1], as_index=False)[columns[0]]  \
            .count() \
            .sort_values(by=columns[0], ascending=False) \
            .rename(columns={columns[0]: f'n_{columns[0]}'}) \
            .reset_index(drop=True)

        item_users.reset_index(inplace=True)

        sns.set_theme(style="ticks")
        fig = sns.lineplot(
            x     = 'index',
            y     = f'n_{columns[0]}',
            data  = item_users
        )
        fig.set_xlabel(columns[1])
