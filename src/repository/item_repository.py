from .entity_repository import EntityRepository
from mapper import ItemMapper


class ItemRepository(EntityRepository):
    def __init__(self, client, mapper): super().__init__(client, mapper, 'items')

