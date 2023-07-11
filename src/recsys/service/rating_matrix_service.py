from enum import Enum

from recsys import util as ut
from recsys.logger import get_logger

RatingMatrixType = Enum('RatingMatrixType', ['USER_ITEM', 'ITEM_USER'])


def to_rating_matrix(df, columns, matrix_type=RatingMatrixType.USER_ITEM):
    if matrix_type == RatingMatrixType.USER_ITEM:
        return ut.df_to_matrix(df, x_col=columns[0], y_col=columns[1], value_col=columns[2])
    elif matrix_type == RatingMatrixType.ITEM_USER:
        return ut.df_to_matrix(df, x_col=columns[1], y_col=columns[0], value_col=columns[2])


class RatingMatrixService:
    def __init__(self):
        self._logger = get_logger(self)

    def __interactions_info(self, df, columns, prefix=''):
        self._logger.info(
            f'{prefix} interactions: {df.shape[0]} - Users: {df[columns[0]].unique().shape[0]}, Items: {df[columns[1]].unique().shape[0]}')

    def create(
            self,
            train_interactions,
            future_interactions,
            columns=('user_seq', 'item_seq', 'rating'),
            matrix_type=RatingMatrixType.USER_ITEM
    ):
        interactions = ut.concat(
            train_interactions[list(columns)],
            future_interactions[list(columns)]
        ).drop_duplicates()

        interactions.to_json('/var/tmp/rec-sys-client/temporal2.json', orient='records')

        self.__interactions_info(interactions, columns, prefix='Train + Predited')

        self._logger.info(f'Compute interactions sparse {matrix_type} matrix...')
        return to_rating_matrix(interactions, columns, matrix_type)

    def __interactions_info(self, df, columns, prefix=''):
        self._logger.info(
            f'{prefix} interactions: {df.shape[0]} - Users: {df[columns[0]].unique().shape[0]}, Items: {df[columns[1]].unique().shape[0]}')
