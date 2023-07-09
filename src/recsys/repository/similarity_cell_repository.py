from .entity_repository import EntityRepository
from recsys.mapper import UserMapper
import pandas as pd


class SimilarityCellRepository(EntityRepository):


    def __init__(self, client, mapper):
        """Constructor

        Args:
            client (api.RecSysApi): a RecSysApi api client.
            mapper (mapper.SimilarityMatrixCellMapper): mapper to map objects between dto-model.
        """

        super().__init__(client, mapper, 'similarity_matrix_cell')


    def add_many(self, cells: pd.DataFrame):
        dtos = [self._mapper.to_dto(row, self._client.host) for _, row in cells.iterrows()]
        return self._client.bulk_add_similarity_cells(dtos)


    def remove(self, id: int):
        """Remove a similar matrix cell by identifier

        Args:
            id (int): A similar matrix cell identifier.
        """
        return self._client.remove_similarity_cell(id)