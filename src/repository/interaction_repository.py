from .entity_repository import EntityRepository
from mapper import InteractionMapper
import pandas as pd


class InteractionRepository(EntityRepository):
    def __init__(self, client, mapper): super().__init__(client, mapper, 'interactions')


    def add_many(self, cells: pd.DataFrame):
        dtos = [self._mapper.to_dto(row, self._client.host) for _, row in cells.iterrows()]
        return self._client.bulk_add_interactions(dtos)
