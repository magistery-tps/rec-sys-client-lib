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


        train_interactions = train_interactions \
            .pipe(self.__interaction_service.filter_users_by_min_interactions, columns, min_n_interactions)

        # Add user/item numeric sequences...
        train_interactions = dt.Sequencer(column='user_id', seq_col_name='user_seq').perform(train_interactions)
        train_interactions = dt.Sequencer(column='item_id', seq_col_name='item_seq').perform(train_interactions)

        self._logger.info(f'Check user_seq: {check_consecutive(train_interactions["user_seq"].unique())}')
        self._logger.info(f'Check item_seq: {check_consecutive(train_interactions["item_seq"].unique())}')

        future_interactions = train_interactions \
            .pipe(self.__interaction_service.unrated_user_item)

        self.__interactions_info(train_interactions, columns, prefix='Train')
        self.__interactions_info(future_interactions, columns, prefix='Future')

        train_predict_fn(train_interactions, future_interactions, columns)

        return future_interactions, train_interactions


    def __interactions_info(self, df, columns, prefix=''):
        self._logger.info(
            f'{prefix} interactions: {df.shape[0]} - Users: {df[columns[0]].unique().shape[0]}, Items: {df[columns[1]].unique().shape[0]}')
