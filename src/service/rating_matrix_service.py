import numpy as np
import util as ut
import pandas as pd
import model as ml
import logging
from enum import Enum


RatingMatrixType = Enum('RatingMatrixType', ['USER_ITEM', 'ITEM_USER'])


class RatingMatrixService:
    def __init__(self, interaction_service):
        self.__interaction_service = interaction_service


    def compute(
        self,
        train_interactions,
        model,
        matrix_type        = RatingMatrixType.USER_ITEM,
        min_n_interactions = 20,
        rating_scale       = [1, 2, 3, 4, 5]
    ):
        train_interactions = train_interactions \
            .pipe(self.__interaction_service.filter_by_rating_scale, rating_scale) \
            .pipe(self.__interaction_service.filter_users_by_min_interactions, min_n_interactions=20)

        future_interactions = train_interactions \
            .pipe(self.__interaction_service.unrated_user_item)

        train_dataset = ml.DatasetFactory.create(train_interactions)

        ml.ModelManager(model).train(train_dataset).predict_inplase(future_interactions)

        all_interactions = ut.concat(train_interactions, future_interactions)

        logging.info(f'Compute interactions sparse {matrix_type} matrix...')
        return self.__to_rating_matrix(all_interactions, matrix_type)


    def __to_rating_matrix(self, df, matrix_type = RatingMatrixType.USER_ITEM):
        if matrix_type == RatingMatrixType.USER_ITEM:
            return ut.df_to_matrix(df, x_col='user_id', y_col='item_id', value_col='rating')
        elif matrix_type == RatingMatrixType.ITEM_USER:
            return ut.df_to_matrix(df, x_col='item_id', y_col='user_id', value_col='rating')