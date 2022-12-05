from .entity_repository import EntityRepository
from mapper import InteractionMapper


class InteractionRepository(EntityRepository):
    def __init__(self, client, mapper): super().__init__(client, mapper, 'interactions')
