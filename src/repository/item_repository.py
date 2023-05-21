from .entity_repository import EntityRepository
from mapper import ItemMapper


class ItemRepository(EntityRepository):


    def __init__(self, client, mapper):
        """Constructor

        Args:
            client (api.RecSysApi): a RecSysApi api client.
            mapper (mapper.ItemMapper): mapper to map objects between dto-model.
        """

        super().__init__(client, mapper, 'items')

