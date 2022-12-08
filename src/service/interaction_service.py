import numpy as np
import api
from repository import InteractionRepository
import util as ut
import seaborn as sns
import multiprocessing as mp
import pandas as pd
import logging


class InteractionService:
    def __init__(self, repository: InteractionRepository):
        self.repository = repository

    def n_interactions_by_user(self, df, min_n_interactions=20):
        return df  \
            .groupby('user_id', as_index=False)['item_id'] \
            .count() \
            .rename(columns={'item_id': 'n_interactions'}) \
            .query('n_interactions >= 20')


    def filter_by_rating_scale(self, df, rating_scale):
        logging.info(f'Filter by ratings scale: {rating_scale}')

        df_filtered = df.pipe(lambda df: df[df['rating'].isin(rating_scale)])

        logging.info(f'Filtered: {(df_filtered.shape[0] / df.shape[0]) * 100:.1f}%')
        return df_filtered


    def filter_users_by_min_interactions(self, df, min_n_interactions=20):
        logging.info(f'Filter by user_n_interactions >= {min_n_interactions}')

        user_ids = self.n_interactions_by_user(df, min_n_interactions).user_id.unique()
        df_filtered = df[df['user_id'].isin(user_ids)]

        logging.info(f'Filtered: {(df_filtered.shape[0] / df.shape[0]) * 100:.1f}%')
        return df_filtered


    def find_all(self, page_size = 50000):
        return pd.DataFrame.from_records(self.repository.find(page_size=page_size))


    def unrated_user_item(self, df, min_rating=1):
        items_by_user = self.items_by_user(df, min_rating)

        all_item_ids = set(df['item_id'].astype(int).unique())

        data = []
        for user_id, rated_item_ids in items_by_user.items():
            for unrated_item_id in (all_item_ids - rated_item_ids):
                data.append({'user_id': user_id, 'item_id': unrated_item_id})

        unrated_interactions = pd.DataFrame(data)

        total = df.user_id.unique().shape[0] * df.item_id.unique().shape[0]
        percent = (unrated_interactions.shape[0] / total) * 100
        logging.info(f'Unrated interactions: {percent:.1f}%')

        return unrated_interactions


    def items_by_user(self, df, min_rating=1):
        items_by_user = {}

        for _, row in df.iterrows():
            if row['rating'] == None or row['rating'] < min_rating:
                continue

            user_id, item_id = row['user_id'].astype(int), row['item_id'].astype(int)

            if user_id not in items_by_user:
                items_by_user[user_id] = set()

            items_by_user[user_id].add(item_id)

        return items_by_user


    def plot_n_users_by_item(self, df):
        item_users = df \
            .groupby('item_id', as_index=False)['user_id']  \
            .count() \
            .rename(columns={'user_id': 'n_users'}) \
            .sort_values(by='n_users', ascending=False) \
            .reset_index(drop=True)

        item_users.reset_index(inplace=True)

        item_users = item_users.rename(columns={'index': 'Items'}) \

        sns.set_theme(style="ticks")
        sns.lineplot(
            x     = 'Items',
            y     = 'n_users',
            data  = item_users
        )
