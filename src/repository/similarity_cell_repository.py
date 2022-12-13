from .entity_repository import EntityRepository
from mapper import UserMapper
import pandas as pd


class SimilarityCellRepository(EntityRepository):
    def __init__(self, client, mapper): super().__init__(client, mapper, 'similarity_matrix_cell')


    def add_many(self, cells: pd.DataFrame):
        dtos = [self._mapper.to_dto(row, self._client.host) for _, row in cells.iterrows()]
        return self._client.bulk_add_similarity_cells(dtos)


    def remove(self, id: int):
        return self._client.remove_similarity_cell(id)