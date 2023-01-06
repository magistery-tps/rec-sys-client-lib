from ..models               import Recommendations, SimilarItemsResult
from .recommender           import Recommender
from .recommender_context   import RecommenderContext
from .recommender_metadata  import RecommenderMetadata
import random


class PopularityRecommender(Recommender):
    def __init__(self, item_service):
        self.__item_service = item_service


    @property
    def metadata(self):
        return RecommenderMetadata(
            id   = 2_000_000,
            name = 'populars',
            title = 'Most Populars',
            description = """
                <strong>Shuffle of most popular items.</strong>
                <br>
                <br>
                Formula:
                <br>
                <strong>popularity = norm(mean(ratings) x norm(count(ratings)))</strong>
            """
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


    def find_similars(self, ctx: RecommenderContext):
        return SimilarItemsResult(self.metadata)