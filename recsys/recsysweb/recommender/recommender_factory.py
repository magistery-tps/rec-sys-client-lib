from .non_scored_popularity_recommender import NonScoredPopularityRecommender
from .popularity_recommender            import PopularityRecommender
from .profile_recommender               import ProfileRecommender
from .cf_recommender                    import CollaborativeFilteringRecommender
from .recommender_ensemble              import RecommenderEnsemble
from .similar_item                      import SimilarItem

from ..models.recommender                   import Recommender               as RecommenderModel
from ..models.recommender_ensemble_config   import RecommenderEnsembleConfig as RecommenderEnsembleConfigModel
from ..models.recommender_ensemble          import RecommenderEnsemble       as RecommenderEnsembleModel
from ..models.recommender_type              import RecommenderType
from singleton_decorator import singleton


@singleton
class RecommenderFactory:
    def __init__(self, ctx): self.ctx = ctx


    def create(self, config):
        if isinstance(config, RecommenderModel):
            return self.__create_recommender(config)
        elif isinstance(config, RecommenderEnsembleModel):
            recommender_configs = RecommenderEnsembleConfigModel.objects.filter(ensemble=config)
            return RecommenderEnsemble(
                config,
                recommender_configs,
                self.ctx.interaction_service,
                recommenders = [self.__create_recommender(rc.recommender) for rc in recommender_configs]
            )
        else:
            raise Error(f'Missing recommender config: {type(config)}')


    def __create_recommender(self, config):
        if config.type == RecommenderType.POPULARS:
            return PopularityRecommender(config, self.ctx.item_service)
        elif config.type == RecommenderType.USER_PROFILE:
            return ProfileRecommender(config, self.ctx.tag_service, self.ctx.item_service)
        elif config.type == RecommenderType.NEW_POPULARS:
            return NonScoredPopularityRecommender(config, self.ctx.item_service)
        elif config.type == RecommenderType.COLLAVORATIVE_FILTERING:
            return CollaborativeFilteringRecommender(config, self.ctx.similarity_matrix_service)
        else:
            raise Error(f'Missing recommender type: {config.type}')
