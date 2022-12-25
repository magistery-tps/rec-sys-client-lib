import numpy as np
import util as ut
import pandas as pd
import model as ml
from logger import get_logger
from enum import Enum
import data as dt


RatingMatrixType = Enum('RatingMatrixType', ['USER_ITEM', 'ITEM_USER'])

def checkConsecutive(l):
    return sorted(l) == list(range(min(l), max(l)+1))

class RatingMatrixService:
    def __init__(self, interaction_service):
        self.__interaction_service = interaction_service
        self._logger = get_logger(self)

    def create(
        self,
        train_interactions,
        model,
        columns            = ('user_seq', 'item_seq', 'rating'),
        matrix_type        = RatingMatrixType.USER_ITEM,
        min_n_interactions = 20,
        rating_scale       = [1, 2, 3, 4, 5],
        progress           = 10
    ):
        train_interactions = train_interactions \
            .pipe(self.__interaction_service.filter_by_rating_scale, columns, rating_scale) \
            .pipe(self.__interaction_service.filter_users_by_min_interactions, columns, min_n_interactions)

        # Add user/item numeric sequences...
        train_interactions = dt.Sequencer(column='user_id', seq_col_name='user_seq').perform(train_interactions)
        train_interactions = dt.Sequencer(column='item_id', seq_col_name='item_seq').perform(train_interactions)

        self._logger.info(f'Check user_seq: {checkConsecutive(train_interactions["user_seq"].unique())}')
        self._logger.info(f'Check item_seq: {checkConsecutive(train_interactions["item_seq"].unique())}')

        future_interactions = train_interactions \
            .pipe(self.__interaction_service.unrated_user_item)


        self.__interactions_info(train_interactions,  columns, prefix='Train')
        self.__interactions_info(future_interactions, columns, prefix='Future')

        train_dataset = ml.DatasetFactory().create(train_interactions, columns)

        ml.ModelManager(model) \
            .train(train_dataset) \
            .predict_inplase(future_interactions, columns, progress)

        all_interactions = ut.concat(train_interactions, future_interactions)

        self.__interactions_info(all_interactions, columns, prefix='Train + Predited')

        self._logger.info(f'Compute interactions sparse {matrix_type} matrix...')
        return self.__to_rating_matrix(all_interactions, columns, matrix_type, progress), train_interactions


    def __to_rating_matrix(self, df, columns, matrix_type = RatingMatrixType.USER_ITEM, progress=10):
        if matrix_type == RatingMatrixType.USER_ITEM:
            return ut.df_to_matrix(df, x_col=columns[0], y_col=columns[1], value_col=columns[2], progress=progress)
        elif matrix_type == RatingMatrixType.ITEM_USER:
            return ut.df_to_matrix(df, x_col=columns[1], y_col=columns[0], value_col=columns[2], progress=progress)

    def __interactions_info(self, df, columns, prefix=''):
        self._logger.info(f'{prefix} interactions: {df.shape[0]} - Users: {df[columns[0]].unique().shape[0]}, Items: {df[columns[1]].unique().shape[0]}')
