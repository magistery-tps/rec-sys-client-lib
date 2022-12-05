import numpy as np
import api
from repository import InteractionRepository
import util as ut
import seaborn as sns
import multiprocessing as mp
import pandas as pd


def user_items_to_df(params):
    user  = params[0]
    items = params[1]
    return pd.DataFrame([{'user_id': user, 'item_id': item} for item in items])


class InteractionService:
    def __init__(self, repository: InteractionRepository):
        self.repository = repository


    def find_all(self, page_size):
        return self.repository.find_all(page_size)

    
    def rated_items_by_user(self, df, min_rating=0):
        result = {}
        for _, row in df.iterrows():
            if row['rating'] != None and row['rating'] > min_rating:
                if row['user_id'] in result:
                    result[row['user_id']].add(row['item_id'])
                else:
                    result[row['user_id']] = set([row['item_id']])
        return result

    def to_matrix(self, df):
        return ut.df_to_matrix(
            df,
            x_col     = 'user_id',
            y_col     = 'item_id',
            value_col = 'rating'
        )

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

    def unrated_distinct_user_item(self, df):
        unrated_items_by_user = self.__unrated_items_by_users(df)
        return self.__distinct_user_item(unrated_items_by_user)

    def __distinct_user_item(self, user_items, processes=20):
        inputs = [(user, items) for user, items in user_items.items()]

        with mp.Pool(processes=processes) as pool:
            results = pool.map(user_items_to_df, inputs)

        return pd.concat(results)

    def __unrated_items_by_users(self, df, min_rating=0):
        all_items           = set(np.unique(df['item_id'].values))
        rated_items_by_user = self.rated_items_by_user(df, min_rating)
        result              = {user: list(all_items-user_rated_items) for user, user_rated_items in rated_items_by_user.items()}

        del rated_items_by_user
        del all_items

        return result