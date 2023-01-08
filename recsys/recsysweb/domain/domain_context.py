from ..models import RecommenderEnsempleEvaluation
from ..service import *
from ..recommender import *
from singleton_decorator import singleton


@singleton
class DomainContext:
    def __init__(self):
        self.evaluation_service        = EvaluationService()
        self.item_service              = ItemService()
        self.tag_service               = TagService()
        self.interaction_service       = InteractionService()
        self.similarity_matrix_service = SimilarityMatrixService()
        self.recommender_factory       = RecommenderFactory(self)
        self.recommender_service       = RecommenderService(self)
