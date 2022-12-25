from ..models import Item, Recommendations
from .recommender import Recommender, RecommenderContext
import random


class PopularityRecommender(Recommender):
    def recommend(self, ctx: RecommenderContext):
        items = Item.objects.all().order_by('popularity')[ctx.shuffle_limit:]

        selected_items = random.sample(list(items), ctx.limit)

        selected_items = sorted(
            selected_items,
            key     = lambda item: item.popularity,
            reverse = True
        )

        return Recommendations(
            id          = 'most_populars',
            name        = 'Most Populars',
            description = """
                <strong>Shuffle of most popular items.</strong>
                <br>
                <br>
                Formula:
                <br>
                <strong>popularity = norm(mean(ratings) x norm(count(ratings)))</strong>
            """,
            items = selected_items
        )
