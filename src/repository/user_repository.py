from .entity_repository import EntityRepository
from mapper import UserMapper


class UserRepository(EntityRepository):


    def __init__(self, client, mapper):
        """Constructor

        Args:
            client (api.RecSysApi): a RecSysApi api client.
            mapper (mapper.UserMapper): mapper to map objects between dto-model.
        """

        super().__init__(client, mapper, 'users')

