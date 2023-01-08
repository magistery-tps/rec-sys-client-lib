from ..models               import Recommendations, SimilarItemsResult
from .recommender           import Recommender, RecommenderCapability
from .recommender_context   import RecommenderContext
from .recommender_metadata  import RecommenderMetadata
import random


class PopularityRecommender(Recommender):
    def __init__(self, config, item_service):
        super().__init__(config)
        self.__item_service = item_service


    @property
    def metadata(self):
        return RecommenderMetadata(
            id          = self.config.id,
            features    = 'Top Populars',
            name        = f'recommender-{self.config.id}',
            title       = self.config.name,
            description = self.config.description,
            position    = self.config.position,
            shuffle     = True
        )

    def recommend(self, ctx: RecommenderContext):
        items = self.__item_service.most_populars(ctx.shuffle_limit)

        selected_items = random.sample(list(items), ctx.limit)

        selected_items = sorted(
            selected_items,
            key     = lambda item: item.popularity,
            reverse = True
        )

        return Recommendations(
            metadata = self.metadata,
            items    = selected_items,
            info     = 'At the moment there are no recommendations.' if len(items) == 0 else ''
        )


    @property
    def capabilities(self):
        return [RecommenderCapability.SHUFFLE_RECOMMEND]