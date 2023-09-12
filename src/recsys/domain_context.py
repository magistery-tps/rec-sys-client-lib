from   recsys.mapper     import *
from   recsys.repository import *
from   recsys.service    import *
from   recsys.job        import *
import recsys.util       as ut
import recsys.api
from   recsys.logger import LoggerBuilder

import warnings
from surprise import SVD, NMF


class DomainContext(metaclass=ut.SingletonMeta):
    """A singleton object that build all src services required into a job a notebook.
    Is a facade that allows to access any src services configured and ready for use.
    """
    def __init__(self, cfg_path = './config.yml'):
        self.cfg = ut.YmlUtil.load(cfg_path)

        self.temp_path = self.cfg.temp_path
        ut.mkdir(self.temp_path)

        LoggerBuilder.build()
        warnings.filterwarnings('ignore')


        self.__client = recsys.api.RecSysApi(self.cfg.api.token, self.cfg.api.host)

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
        self.__interaction_service           = InteractionService(self.__interaction_repository)
        self.__interaction_inference_service = InteractionInferenceService(self.__interaction_service)
        self.__item_service                  = ItemService(self.__item_repository)

        self.__rating_matrix_service     = RatingMatrixService()
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
    def describe(self):
        return list(filter(lambda it: not (it.startswith('_') or it == 'describe'), dir(self)))


    @property
    def api(self)-> recsys.api.RecSysApi:
        """Return a singleton api.RecSysApi instance. This is the more deeper layer into IOC context.

        Returns:
            api.RecSysApi: a REST API client.
        """
        return self.__client


    @property
    def interaction_service(self)-> InteractionService:
        """Return a single instance of InteractionService.

        Returns:
            InteractionService: An instance of InteractionService.
        """
        return self.__interaction_service


    @property
    def interaction_inference_service(self)-> InteractionInferenceService:
        """Return a single instance of InteractionInferenceService.

        Returns:
            InteractionInferenceService: An instance of InteractionInferenceService.
        """
        return self.__interaction_inference_service


    @property
    def item_service(self):
        """Return a single instance of ItemService.

        Returns:
            ItemService: An instance of ItemService.
        """
        return self.__item_service


    @property
    def rating_matrix_service(self)->RatingMatrixService:
        """Return a single instance of RatingMatrixService.

        Returns:
            RatingMatrixService: An instance of RatingMatrixService.
        """
        return self.__rating_matrix_service


    @property
    def similarity_service(self)->SimilarityService:
        """Return a single instance of SimilarityService.

        Returns:
            SimilarityService: An instance of SimilarityService.
        """
        return self.__similarity_service


    @property
    def similarity_matrix_service(self)->SimilarityMatrixService:
        """Return a single instance of SimilarityMatrixService.

        Returns:
            SimilarityMatrixService: An instance of SimilarityMatrixService.
        """
        return self.__similarity_matrix_service


    @property
    def recommender_service(self):
        """Return a single instance of RecommenderService.

        Returns:
            RecommenderService: An instance of RecommenderService.
        """
        return self.__recommender_service


    @property
    def svd_distance_matrix_job(self)->SurpriseDistanceMatrixJob:
        """Return a single instance of SurpriseDistanceMatrixJob using a SVD model to predict future user interactions.

        Returns:
            RecommenderService: An instance of RecommenderService.
        """
        return self.__svd_distance_matrix_job


    @property
    def nmf_distance_matrix_job(self)->SurpriseDistanceMatrixJob:
        """Return a single instance of SurpriseDistanceMatrixJob using a NFM model to predict future user interactions.

        Returns:
            RecommenderService: An instance of RecommenderService.
        """
        return self.__nmf_distance_matrix_job


    def bert_item_distance_matrix_job(self, model)->BertItemDistanceMatrixJob:
        """Return a single instance of BertItemDistanceMatrixJob used to build item-to-item similarity matrix.

        Returns:
            BertItemDistanceMatrixJob: An instance of BertItemDistanceMatrixJob.
        """
        return self.__bert_item_distance_matrix_job[model]


    @property
    def user_repository(self)->UserRepository:
        """Return a single instance of UserRepository.

        Returns:
            UserRepository: An instance of UserRepository.
        """
        return self.__user_repository


    @property
    def item_repository(self)->ItemRepository:
        """Return a single instance of ItemRepository.

        Returns:
            ItemRepository: An instance of ItemRepository.
        """
        return self.__item_repository


    @property
    def interaction_repository(self)->InteractionRepository:
        """Return a single instance of InteractionRepository.

        Returns:
            InteractionRepository: An instance of InteractionRepository.
        """
        return self.__interaction_repository


    @property
    def similarity_matrix_repository(self)->SimilarityMatrixRepository:
        """Return a single instance of SimilarityMatrixRepository.

        Returns:
            SimilarityMatrixRepository: An instance of SimilarityMatrixRepository.
        """
        return self.__similarity_matrix_repository


    @property
    def similarity_cell_repository(self)->SimilarityCellRepository:
        """Return a single instance of SimilarityCellRepository.

        Returns:
            SimilarityCellRepository: An instance of SimilarityCellRepository.
        """
        return self.__similarity_cell_repository
