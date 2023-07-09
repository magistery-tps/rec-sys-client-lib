from .entity_repository import EntityRepository
from recsys.mapper import InteractionMapper
import pandas as pd


class InteractionRepository(EntityRepository):
    def __init__(self, client, mapper):
        """Constructor

        Args:
            client (api.RecSysApi): a RecSysApi api client.
            mapper (mapper.InteractionMapper): mapper to map objects between dto-model.
        """

        super().__init__(client, mapper, 'interactions')

    def add_many(self, cells: pd.DataFrame):
        """
        Allows to add a list of user interactions from a pandas DataFrame. DataFrame must have next columns:

        row =  {\n
            'user'              : int user id,\n
            'item'              : int item id,\n
            'rating'            : float,\n
            'suitable_to_train' : bool\n
        }

        Args:
            cells (pd.DataFrame): A DataFrame with user interaction as rows.

        Returns:
            ItemResponse: an ItemResponse object.
        """

        dtos = [self._mapper.to_dto(row, self._client.host) for _, row in cells.iterrows()]
        return self._client.bulk_add_interactions(dtos)