from ..models               import Recommendations, SimilarItemsResult
from .recommender           import Recommender
from .recommender_context   import RecommenderContext
from .recommender_metadata  import RecommenderMetadata
from .recommender_capability    import RecommenderCapability


class RecommenderEnsemble(Recommender):
    def __init__(self, config, ensemble_configs, interaction_service, recommenders):
        super().__init__(config)
        self.__interaction_service = interaction_service
        self.__ensemble_configs    = ensemble_configs
        self.__recommenders        = recommenders
        self.__metadata            = RecommenderMetadata(
            id          = self.config.id,
            name        = f'recommender-{self.config.id}',
            features    = 'Ensemble | ' + ' | '.join([r.metadata.features for r in self.__recommenders]),
            title       = 'Recommendations for you',
            description = self.config.description,
            position    = self.config.position
        )


    @property
    def metadata(self): return self.__metadata


    def __select_recommender(self, user):
        n_user_interactions = self.__interaction_service.count_by_user(user)

        for idx, cfg in enumerate(self.__ensemble_configs):
            to_n_interactions = n_user_interactions if cfg.active_to_n_user_iterations == 0 else cfg.active_to_n_user_iterations

            if cfg.active_from_n_user_iterations <= n_user_interactions and \
                to_n_interactions >= n_user_interactions:
                recommender = self.__recommenders[idx]
                self.metadata.active_nested_metadata = recommender.metadata
                self.metadata.n_items_by_session = cfg.n_items_by_session
                return recommender


    def recommend(self, ctx: RecommenderContext):
        return self.__build_result(self.__select_recommender(ctx.user).recommend(ctx))


    def find_similars(self, ctx: RecommenderContext):
        result = self.__select_recommender(ctx.user).find_similars(ctx)
        return SimilarItemsResult(self.metadata, result.items)


    @property
    def capabilities(self):
        return [RecommenderCapability.RECOMMEND, RecommenderCapability.SIMILARS]


    def __build_result(self, result):
        return Recommendations(
            metadata = self.metadata,
            items    = result.items,
            info     = result.info
        )

