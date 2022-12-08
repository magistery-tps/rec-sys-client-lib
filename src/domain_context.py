from   mapper     import *
from   repository import *
from   service    import *
import util       as ut
import api
from logger import LoggerBuilder
import warnings


class DomainContext(metaclass=ut.SingletonMeta):
    def __init__(self, token, host):
        LoggerBuilder.build()
        warnings.filterwarnings('ignore')

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
        self.__rating_matrix_service  = RatingMatrixService(self.__interaction_service)
        self.__similarity_service      = SimilarityService()


    @property
    def interaction_service(self): return self.__interaction_service


    @property
    def rating_matrix_service(self): return self.__rating_matrix_service


    @property
    def similarity_service(self): return self.__similarity_service
