import numpy as np
import util as ut
import pandas as pd
import model as ml
from logger import get_logger
from enum import Enum
import api
import mapper


class SimilarityMatrixService:
    def __init__(
        self,
        matrix_repository,
        cell_repository,
        interaction_service,
        similarity_service
    ):
        self.__matrix_repository   = matrix_repository
        self.__cell_repository     = cell_repository
        self.__interaction_service = interaction_service
        self.__similarity_service  = similarity_service
        self._logger               = get_logger(self)


    def update_user_similarity_matrix(
        self,
        user_similarities,
        interactions,
        name,
        n_most_similars = 50
    ):
        # Get similarity matrix...
        similarity_matrix = self.create_or_get(name, type = api.SimilarityMatrixType.USER_TO_USER)

        similarity_matrix.version += 1

        # Map sequences to ids
        user_seq_by_id = self.__interaction_service.seq_by_id(interactions, entity='user')

        # Prepare cells...
        cells = self.__similarity_service.filter_most_similars(
            user_similarities,
            column = 'user_a',
            n      = n_most_similars
        ).rename(columns={'user_a': 'row', 'user_b': 'column'})
        cells['row']    = cells['row'].apply(lambda seq: user_seq_by_id[seq])
        cells['column'] = cells['column'].apply(lambda seq: user_seq_by_id[seq])

        self.add_cells_and_update(similarity_matrix, cells)

        # Remove previous matrix version after add new version cells...
        self.__matrix_repository.remove_previous_versions(similarity_matrix.id)

        return similarity_matrix

    def update_item_similarity_matrix(
        self,
        item_similarities,
        interactions,
        name,
        n_most_similars = 50
    ):
        # Get similarity matrix...
        similarity_matrix = self.create_or_get(name, type = api.SimilarityMatrixType.ITEM_TO_ITEM)

        similarity_matrix.version += 1

        # Map sequences to ids...
        item_seq_by_id = self.__interaction_service.seq_by_id(interactions, entity='item')

        # Prepare most similar cells...
        cells = self.__similarity_service.filter_most_similars(
            item_similarities,
            column = 'item_a',
            n      = n_most_similars
        ).rename(
            columns={'item_a': 'row', 'item_b': 'column'}
        )
        cells['row']    = cells['row'].apply(lambda seq: item_seq_by_id[seq])
        cells['column'] = cells['column'].apply(lambda seq: item_seq_by_id[seq])

        self.add_cells_and_update(similarity_matrix, cells)

        # Remove previous matrix version after add new version cells...
        self.__matrix_repository.remove_previous_versions(similarity_matrix.id)

        return similarity_matrix

    def add_cells_and_update(self, similarity_matrix, cells):
        """
            Add cells and update simialrity matrix fields.
        """
        self.add_cells(similarity_matrix, cells)
        self.update(similarity_matrix)


    def create_or_get(
        self,
        name : str,
        type : api.SimilarityMatrixType,
        desc : str = None
    ):
        if desc is None:
            desc = name

        query={'name': name, 'type': str(type.value)}

        models = self.__matrix_repository.find(query)

        if len(models) > 0 and models[0].name == name:
            self._logger.info(f'Already exists {name} {type} matrix.')
            return models[0]
        else:
            self._logger.info(f'Insert {name} {type} matrix.')
            return self.__matrix_repository.add(name, type, desc)


    def update(self, model): return self.__matrix_repository.update(model)


    def add_cells(self, matrix: mapper.Model, cells: pd.DataFrame, page_size=10_000):
        cells['matrix']  = matrix.id
        cells['version'] = matrix.version

        iterator = ut.DataFramePaginationIterator(cells, page_size=page_size)
        [self.__cell_repository.add_many(page) for page in iterator]

