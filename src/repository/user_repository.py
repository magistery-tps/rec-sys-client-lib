from .entity_repository import EntityRepository
from mapper import UserMapper


class UserRepository(EntityRepository):
    def __init__(self, client, mapper): super().__init__(client, mapper, 'user')

