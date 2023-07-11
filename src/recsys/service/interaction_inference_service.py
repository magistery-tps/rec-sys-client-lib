from enum import Enum

from recsys import data as dt, util as ut, model as ml
import numpy as np
from recsys.logger import get_logger


def check_consecutive(l):
    return sorted(l) == list(range(min(l), max(l) + 1))


class InteractionInferenceService:
    def __init__(self, interaction_service):
        self.__interaction_service = interaction_service
        self._logger = get_logger(self)

    def predict(
            self,
            train_interactions,
            train_predict_fn,
            columns=('user_seq', 'item_seq', 'rating'),
            min_n_interactions=20,
            rating_scale=np.arange(3, 6, 0.5)
    ):
        """Predict future interactions given an incomplete list of user interactions.
        Train a given model with an incomplete list of user interactions to predict missing user interactions.
        It only consider user with min_n_interactions and also user interactions with ratings contained into rating_scale range.

        Args:
            train_interactions (pd.DataFrame): Current user interactions DataFrame used to predict missing interactions.
            train_predict_fn (function): It function train a ML model an predict future interactions rating.
            columns (tuple, optional): Column names that represent user id , item id an rating. The order is important. Defaults to ('user_seq', 'item_seq', 'rating
            min_n_interactions (int, optional): Filter user with a minimum number of interactions. Defaults to 20.
            rating_scale (int list, optional): rating values to filter. Defaults to np.arange(3, 6, 0.5).

        Returns:
            (future_interactions, selected_train_interactions)
        """
        train_interactions = train_interactions \
            .pipe(self.__interaction_service.filter_by_rating_scale, columns, rating_scale)


        self.check_user(train_interactions, 5000, 'step 1')

        train_interactions = train_interactions \
            .pipe(self.__interaction_service.filter_users_by_min_interactions, columns, min_n_interactions)

        self.check_user(train_interactions, 5000, 'step 1')

        # self._logger.info(train_interactions['user_id'].unique())

        # Add user/item numeric sequences...
        train_interactions = dt.Sequencer(column='user_id', seq_col_name='user_seq').perform(train_interactions)
        train_interactions = dt.Sequencer(column='item_id', seq_col_name='item_seq').perform(train_interactions)

        self.check_user(train_interactions, 5000, 'step 3')

        self._logger.info(f'Check user_seq: {check_consecutive(train_interactions["user_seq"].unique())}')
        self._logger.info(f'Check item_seq: {check_consecutive(train_interactions["item_seq"].unique())}')

        future_interactions = train_interactions \
            .pipe(self.__interaction_service.unrated_user_item)

        self._logger.info(f'Future columns: {future_interactions.columns}')

        self.__interactions_info(train_interactions, columns, prefix='Train')
        self.__interactions_info(future_interactions, columns, prefix='Future')

        train_predict_fn(train_interactions, future_interactions, columns)

        self.check_user(future_interactions, 461, 'step 4', field = 'user_seq')

        return future_interactions, train_interactions

    def __interactions_info(self, df, columns, prefix=''):
        self._logger.info(
            f'{prefix} interactions: {df.shape[0]} - Users: {df[columns[0]].unique().shape[0]}, Items: {df[columns[1]].unique().shape[0]}')


    def check_user(self, df, value, step, field = 'user_id'):
        result = df[df[field] == value]

        if result.shape[0] > 0:
            self._logger.info(f'{step}: USER {value} NO FILTERED!. Count: {result.shape[0]}')
            self._logger.info(f'user_seq: {result["user_seq"].unique()[0]}')
            try:
                self._logger.info(f'user_id: {result["user_id"].unique()[0]}')
            except:
                pass
        else:
            self._logger.info(f'{step}: USER {value} YES FILTERED!')