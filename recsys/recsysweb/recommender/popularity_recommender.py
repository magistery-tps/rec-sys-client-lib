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
            name        = 'Most Populars',
            description = """
                Shuffle of most popular items.
                <br>
                Formula:
                <br>
                <strong>item_popularity = min_max_norm(mean(item_ratings) * min_max_norm(count(item_interactions)))</strong>
            """,
            items = selected_items
        )
