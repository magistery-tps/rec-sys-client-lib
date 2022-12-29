from ..models import Item, Recommendations
from .recommender import Recommender, RecommenderContext, RecommenderMetadata
import random


class PopularityRecommender(Recommender):
    @property
    def metadata(self):
        return RecommenderMetadata(
            id   = 2_000_000,
            name = 'Most Populars',
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
        items = Item.objects.all().order_by('popularity')[ctx.shuffle_limit:]

        selected_items = random.sample(list(items), ctx.limit)

        selected_items = sorted(
            selected_items,
            key     = lambda item: item.popularity,
            reverse = True
        )

        return Recommendations(
            metadata = self.metadata,
            items    = selected_items,
            info     = 'Not found recommendations!' if len(items) == 0 else ''
        )


    def find_similars(self, ctx: RecommenderContext):
        return []