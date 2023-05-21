from .entity_repository import EntityRepository
from mapper import InteractionMapper
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

        row =  {
            'user'              : int user id,
            'item'              : int item id,
            'rating'            : float,
            'suitable_to_train' : bool
        }

        Args:
            cells (pd.DataFrame): A DataFrame with user interaction as rows.

        Returns:
            ItemResponse: an ItemResponse object.
        """

        dtos = [self._mapper.to_dto(row, self._client.host) for _, row in cells.iterrows()]
        return self._client.bulk_add_interactions(dtos)