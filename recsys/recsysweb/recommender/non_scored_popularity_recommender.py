from ..models               import Recommendations, SimilarItemsResult
from .recommender           import Recommender
from .recommender_context   import RecommenderContext
from .recommender_metadata  import RecommenderMetadata

import random


class NonScoredPopularityRecommender(Recommender):
    def __init__(self, item_service):
        self.__item_service = item_service


    @property
    def metadata(self):
        return RecommenderMetadata(
            id   = 1_000_000,
            name = 'new-populars',
            title = 'Populars you could read',
            description = """<strong>Recommendation Strategy</strong><br>
                Shuffle of user unrated popular items. The idea is recommend popular items that user has not seen yet.
                <br>
                <br>
                Popularity Formula:
                <br>
                popularity = norm(mean(ratings) x norm(count(ratings)))
                <br>
                <br>
                <strong>Item Similarity Strategy</strong><br>
                It recommender has not an item-to-item similarity strategy."""
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


    def find_similars(self, ctx: RecommenderContext):
        return SimilarItemsResult(self.metadata)
