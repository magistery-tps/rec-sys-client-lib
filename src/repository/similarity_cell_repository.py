from .entity_repository import EntityRepository
from mapper import UserMapper
import pandas as pd


class SimilarityCellRepository(EntityRepository):
    def __init__(self, client, mapper): super().__init__(client, mapper, 'similarity_matrix_cell')

    def add(
        self,
        row     : int,
        column  : int,
        value   : float,
        matrix  : int,
        version : int = 0,
    ):
        self._client.add_similarity_cell(row, column, value, version)


    def bulk_add(self, cells: pd.DataFrame):
        body = [self._mapper.to_dto(row) for _, row in cells.iterrows()]
        return self._client.bulk_add_similarity_cells(body)


    def remove(self, id: int):
        return self._client.remove_similarity_cell(id)