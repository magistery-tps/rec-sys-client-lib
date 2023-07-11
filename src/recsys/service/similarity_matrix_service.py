import pandas as pd
from recsys import util as ut, api, mapper
from recsys.logger import get_logger


class SimilarityMatrixService:
    def __init__(
            self,
            matrix_repository,
            cell_repository,
            interaction_service,
            similarity_service
    ):
        self.__matrix_repository = matrix_repository
        self.__cell_repository = cell_repository
        self.__interaction_service = interaction_service
        self.__similarity_service = similarity_service
        self._logger = get_logger(self)

    def update_user_similarity_matrix(
            self,
            user_similarities,
            interactions,
            name,
            n_most_similars=50
    ):
        """Update a similarity matrix with a new version of cells. Each update create a new similarity matrix cells version
         associated with a unique similarity matrix entity.

        Args:
            name (str): A similarity matrix name. It's a similarity matrix identifier.
            user_similarities (pd.DataFrame): A table with columns[user_a, user_b, similarity].
            interactions (ps.DataFrame): A table with columns=[user_id, user_seq, item_id, item_seq]. It contains real(non-predicted) user interactions.
            n_most_similars (int, optional): Take into account only n_most_similars users. Defaults to 50.

        Returns:
            Model: A new or updated similarity matrix model.
        """
        # Get similarity matrix...
        similarity_matrix = self.__create_or_get(name, type=api.SimilarityMatrixType.USER_TO_USER)

        similarity_matrix.version += 1

        interactions.to_json('/var/tmp/rec-sys-client/temporal.json', orient='records')

        # Map sequences to ids
        user_id_by_seq = ut.id_by_seq(interactions, entity='user')

        self._logger.info(f'User seq 461, id: {user_id_by_seq[461]}.')

        self._logger.info(f'Map: {user_id_by_seq}.')

        # Prepare cells...
        cells = self.__similarity_service.filter_most_similars(
            user_similarities,
            columns=['user_a', 'user_b'],
            n=n_most_similars
        )

        cells = cells.rename(columns={'user_a': 'row', 'user_b': 'column'})

        cells['row'] = cells['row'].apply(lambda seq: user_id_by_seq[seq])
        cells['column'] = cells['column'].apply(lambda seq: user_id_by_seq[seq])

        self.__add_cells_and_update(similarity_matrix, cells)

        # Remove previous matrix version after add new version cells...
        self.__matrix_repository.remove_previous_versions(similarity_matrix.id)

        return similarity_matrix

    def update_item_similarity_matrix(
            self,
            item_similarities,
            interactions,
            name,
            n_most_similars=50
    ):
        """
        Update a similarity matrix with a new version of cells. Each update create a new similarity matrix cells version
        associated with a unique similarity matrix entity.

        Args:
            name (str): A similarity matrix name. It's a similarity matrix identifier.
            user_similarities (pd.DataFrame): A table with columns[item_a, item_b, similarity]..
            interactions (ps.DataFrame): A table with columns=[user_id, user_seq, item_id, item_seq]. It contains real(non-predicted) user interactions.
            n_most_similars (int, optional): Take into account only n_most_similars users. Defaults to 50.

        Returns:
            Model: A new or updated similarity matrix model.
        """
        # Get similarity matrix...
        similarity_matrix = self.__create_or_get(name, type=api.SimilarityMatrixType.ITEM_TO_ITEM)

        similarity_matrix.version += 1

        # Map sequences to ids...
        item_id_by_seq = ut.id_by_seq(interactions, entity='item')
        # breakpoint()

        # Prepare most similar cells...
        cells = self.__similarity_service.filter_most_similars(
            item_similarities,
            columns=['item_a', 'item_b'],
            n=n_most_similars
        ).rename(
            columns={'item_a': 'row', 'item_b': 'column'}
        )
        cells = cells.rename(columns={'item_a': 'row', 'item_b': 'column'})
        cells['row'] = cells['row'].apply(lambda seq: item_id_by_seq[seq])
        cells['column'] = cells['column'].apply(lambda seq: item_id_by_seq[seq])

        self.__add_cells_and_update(similarity_matrix, cells)

        # Remove previous matrix version after add new version cells...
        self.__matrix_repository.remove_previous_versions(similarity_matrix.id)

        return similarity_matrix


    def __add_cells_and_update(self, similarity_matrix, cells):
        """
            Add cells and update similarity matrix fields.
        """
        self.__add_cells(similarity_matrix, cells)
        self.__update(similarity_matrix)


    def __create_or_get(
            self,
            name: str,
            type: api.SimilarityMatrixType,
            desc: str = None
    ):
        if desc is None:
            desc = name

        query = {'name': name, 'type': str(type.value)}

        models = self.__matrix_repository.find(query)

        if len(models) > 0 and models[0].name == name:
            self._logger.info(f'Already exists {name} {type} matrix.')
            return models[0]
        else:
            self._logger.info(f'Insert {name} {type} matrix.')
            return self.__matrix_repository.add(name, type, desc)


    def __update(self, model):
        return self.__matrix_repository.update(model)


    def __add_cells(self, matrix: mapper.Model, cells: pd.DataFrame, page_size=5_000):
        cells['matrix'] = matrix.id
        cells['version'] = matrix.version

        iterator = ut.DataFramePaginationIterator(cells, page_size=page_size)
        [self.__cell_repository.add_many(page) for page in iterator]
