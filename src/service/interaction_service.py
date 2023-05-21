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


    def n_interactions_by_user(
        self,
        df,
        columns            = ('user_seq', 'item_seq', 'rating'),
        min_n_interactions = 20
    ):
        """Query into a given pd.DataFrame the number of interactions by user filtered by min_n_interactions count.

        Args:
            df (pd.DataFrame): DataFrame with user interactions.
            columns (tuple, optional): Column names that represent user id , item id an rating. The order is important. Defaults to ('user_seq', 'item_seq', 'rating').
            min_n_interactions (int, optional): Filter user with a minimum number of interactions. Defaults to 20.

        Returns:
            pd.DataFrame: A filtered table.
        """
        return df  \
            .groupby(columns[0], as_index=False)[columns[1]] \
            .count() \
            .rename(columns={columns[1]: 'n_interactions'}) \
            .query('n_interactions >= 20')


    def filter_by_rating_scale(
        self,
        df,
        columns      = ('user_seq', 'item_seq', 'rating'),
        rating_scale = np.arange(3, 6, 0.5)
    ):
        """Filter a given interactions pd.DataFrame by ratings contained into rating_scale argument.

        Args:
            df (pd.DataFrame): DataFrame with user interactions.
            columns (tuple, optional): Column names that represent user id , item id an rating. The order is important. Defaults to ('user_seq', 'item_seq', 'rating').
            rating_scale (int list, optional): rating values to filter. Defaults to np.arange(3, 6, 0.5).

        Returns:
            pd.DataFrame: Input pd.DataFrame filtered.
        """
        self._logger.info(f'Filter by {columns[2]} scale: {rating_scale}')

        df_filtered = df.pipe(lambda df: df[df[columns[2]].isin(rating_scale)])

        self._logger.info(f'Excluded: {(1- (df_filtered.shape[0] / df.shape[0])) * 100:.1f}%')
        return df_filtered


    def filter_users_by_min_interactions(
        self,
        df,
        columns            = ('user_seq', 'item_seq', 'rating'),
        min_n_interactions = 20,
    ):
        """Filter user into given interactions pd.DataFrame with min_n_interactions.

        Args:
            df (pd.DataFrame): DataFrame with user interactions.
            columns (tuple, optional): Column names that represent user id , item id an rating. The order is important. Defaults to ('user_seq', 'item_seq', 'rating').
            min_n_interactions (int, optional): Filter user with a minimum number of interactions. Defaults to 20.

        Returns:
            pd.DataFrame: Input pd.DataFrame filtered.
        """
        self._logger.info(f'Filter interactions by user_n_interactions >= {min_n_interactions}')

        user_ids = self.n_interactions_by_user(df, columns, min_n_interactions)[columns[0]].unique()
        df_filtered = df[df[columns[0]].isin(user_ids)]

        self._logger.info(f'Excluded: {(1 - (df_filtered.shape[0] / df.shape[0])) * 100:.1f}% ({df.shape[0] - df_filtered.shape[0]})')

        return df_filtered


    def add_many(self, interactions: pd.DataFrame, page_size=10):
        """Allows to add a list of user interactions from a pandas DataFrame. DataFrame must have next columns:

        Examples:
            row =  {
                'user'              : int user id,
                'item'              : int item id,
                'rating'            : float,
                'suitable_to_train' : bool
            }

        Args:
            interactions (pd.DataFrame): A DataFrame with user interaction as rows.
            page_size(int, optional): Page size user to push interactions as a bulk insert.
        """
        iterator = ut.DataFramePaginationIterator(interactions, page_size=page_size)
        [self.repository.add_many(page) for page in iterator]


    def find_all(self, page_size = 5000):
        """Query all user interactions.

        Args:
            page_size (int, optional): Page size used to fetch user interactions. Defaults to 5000.

        Returns:
            pd.DataFrame: A pd.DataFrame with all user interactions.
        """
        return pd.DataFrame.from_records(self.repository.find(page_size=page_size))


    def unrated_user_item(
        self,
        df,
        columns    = ('user_seq', 'item_seq', 'rating'),
        min_rating = 1
    ):
        """Returns interactions that users has not performed yet.

        Args:
            df (ps.DataFrame): An user interactions pd.DataFrame.
            columns (tuple, optional): Column names that represent user id , item id an rating. The order is important. Defaults to ('user_seq', 'item_seq', 'rating').
            min_rating (int, optional): A user interaction with min_rating is consider a real user interaction. Defaults to 1.

        Returns:
            pd.DataFrame: A DataFrame of (user_id, item_id) tuples.
        """
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
        """Return a dict with user_id key and a list of items as value.
        Item query all items rated for each user. Considering min_raging
        interactions as a real interaction.

        Args:
            df (ps.DataFrame): An user interactions pd.DataFrame.
            columns (tuple, optional): Column names that represent user id , item id an rating. The order is important. Defaults to ('user_seq', 'item_seq', 'rating').
            min_rating (int, optional): A user interaction with min_rating is consider a real user interaction. Defaults to 1.

        Returns:
            dict: a dist is (user_id, [item_id]) tuples.
        """
        items_by_user = {}

        for _, row in df.iterrows():
            if row[columns[2]] == None or row[columns[2]] < min_rating:
                continue

            user_id, item_id = row[columns[0]], row[columns[1]]

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

