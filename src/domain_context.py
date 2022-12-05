from   mapper     import *
from   repository import *
from   service    import *
import util       as ut
import api


class DomainContext(metaclass=ut.SingletonMeta):
    def __init__(self, token, host):
        client  = api.RecSysApi(token, host)

        # Mappers
        user_mapper        = UserMapper()
        item_mapper        = ItemMapper()
        interaction_mapper = InteractionMapper()

        # Repositories
        self.__user_repository        = UserRepository(client, user_mapper)
        self.__item_repository        = ItemRepository(client, item_mapper)
        self.__interaction_repository = InteractionRepository(client, interaction_mapper)

        # Services
        self.__interaction_service    = InteractionService(self.__interaction_repository)

    @property
    def user_repository(self): return self.__user_repository

    @property
    def item_repository(self): return self.__item_repository

    @property
    def interaction_repository(self): return self.__interaction_repository

    @property
    def interaction_service(self): return self.__interaction_service
