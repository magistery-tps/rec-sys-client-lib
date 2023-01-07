from ..models               import Recommendations, SimilarItemsResult
from .recommender           import Recommender
from .recommender_context   import RecommenderContext
from .recommender_metadata  import RecommenderMetadata

import random


class NonScoredPopularityRecommender(Recommender):
    def __init__(self, config, item_service):
        super().__init__(config)
        self.__item_service = item_service


    @property
    def metadata(self):
        return RecommenderMetadata(
            id          = self.config.id,
            name        = f'recommender-{self.config.id}',
            title       = self.config.name,
            description = self.config.description,
            position    = self.config.position
        )


    def recommend(self, ctx: RecommenderContext):
        user_unrated_items = self.__item_service.unrated_by(ctx.user, ctx.shuffle_limit)
 
        selected_items = random.sample(list(user_unrated_items), ctx.limit)

        selected_items = sorted(
            selected_items,
            key     = lambda item: item.popularity,
            reverse = True
        )

        return Recommendations(
            metadata = self.metadata,
            items    = selected_items,
            info     = 'At the moment there are no recommendations.' if len(user_unrated_items) == 0 else ''
        )
