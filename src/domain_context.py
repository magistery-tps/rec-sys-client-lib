from   mapper     import *
from   repository import *
from   service    import *
from   job        import *
import util       as ut
import api
from logger import LoggerBuilder
import warnings
from surprise import SVD, NMF


class DomainContext(metaclass=ut.SingletonMeta):
    def __init__(self, cfg_path = './config'):
        cfg = ut.YmlUtil.load(cfg_path)

        self.temp_path = cfg.temp_path
        ut.mkdir(self.temp_path)

        LoggerBuilder.build()
        warnings.filterwarnings('ignore')


        self.__client = api.RecSysApi(cfg.api.token, cfg.api.host)

        # Mappers
        user_mapper                   = UserMapper()
        item_mapper                   = ItemMapper()
        interaction_mapper            = InteractionMapper()
        similarity_matrix_mapper      = SimilarityMatrixMapper()
        similarity_matrix_cell_mapper = SimilarityMatrixCellMapper()
        recommender_mapper            = RecommenderMapper()


        # Repositories
        self.__user_repository                   = UserRepository(self.__client, user_mapper)
        self.__item_repository                   = ItemRepository(self.__client, item_mapper)
        self.__interaction_repository            = InteractionRepository(
            self.__client,
            interaction_mapper
        )
        self.__similarity_matrix_repository      = SimilarityMatrixRepository(
            self.__client,
            similarity_matrix_mapper
        )
        self.__similarity_cell_repository = SimilarityCellRepository(
            self.__client,
            similarity_matrix_cell_mapper
        )
        self.__recommender_repository = RecommenderRepository(
            self.__client,
            recommender_mapper
        )

        # Services
        self.__interaction_service       = InteractionService(self.__interaction_repository)
        self.__item_service              = ItemService(self.__item_repository)
        self.__rating_matrix_service     = RatingMatrixService(self.__interaction_service)
        self.__similarity_service        = SimilarityService()
        self.__similarity_matrix_service = SimilarityMatrixService(
            self.__similarity_matrix_repository,
            self.__similarity_cell_repository,
            self.__interaction_service,
            self.__similarity_service
        )
        self.__recommender_service  = RecommenderService(self.__recommender_repository)

        # Jobs
        self.__svd_distance_matrix_job = SurpriseDistanceMatrixJob(
            self,
            model            = SVD(),
            recommender_name = 'SVD'
        )
        self.__nmf_distance_matrix_job = SurpriseDistanceMatrixJob(
            self,
            model            = NMF(),
            recommender_name = 'NMF'
        )


        models = [
            'all-MiniLM-L6-v2',
            'all-MiniLM-L12-v2',
            'multi-qa-mpnet-base-dot-v1',
            'all-mpnet-base-v2'
        ]

        self.__bert_item_distance_matrix_job = {
            model: BertItemDistanceMatrixJob(self, model) for model in models
        }



    @property
    def api(self): return self.__client


    @property
    def interaction_service(self): return self.__interaction_service


    @property
    def item_service(self): return self.__item_service


    @property
    def rating_matrix_service(self): return self.__rating_matrix_service


    @property
    def similarity_service(self): return self.__similarity_service


    @property
    def similarity_matrix_service(self): return self.__similarity_matrix_service


    @property
    def recommender_service(self): return self.__recommender_service


    @property
    def svd_distance_matrix_job(self): return self.__svd_distance_matrix_job


    @property
    def nmf_distance_matrix_job(self): return self.__nmf_distance_matrix_job


    def bert_item_distance_matrix_job(self, model):
        return self.__bert_item_distance_matrix_job[model]


    @property
    def user_repository(self): return self.__user_repository


    @property
    def item_repository(self): return self.__item_repository


    @property
    def interaction_repository(self): return self.__interaction_repository


    @property
    def similarity_matrix_repository(self): return self.__similarity_matrix_repository


    @property
    def similarity_cell_repository(self): return self.__similarity_cell_repository
