from ..models import Item, Recommendations
from .recommender import Recommender, RecommenderContext
import random


class NonScoredPopularityRecommender(Recommender):
    def recommend(self, ctx: RecommenderContext):
        items = Item.objects.raw(
            """
                SELECT
                    DISTINCT
                    id,
                    name,
                    description,
					image,
                    popularity
                FROM
                    recsysweb_item
                WHERE
                    id NOT IN (
                        SELECT
                            DISTINCT i.item_id
                        FROM
                            recsysweb_interaction AS i
                        WHERE
                            i.user_id = :USER_ID
                    )
                GROUP BY
                    id
                ORDER BY
                    popularity DESC
                LIMIT :LIMIT
            """ \
                .replace('\n', ' ') \
                .replace(':USER_ID', str(ctx.user.id)) \
                .replace(':LIMIT', str(ctx.shuffle_limit))
        )

        selected_items = random.sample(list(items), ctx.limit)

        selected_items = sorted(
            selected_items,
            key     = lambda item: item.popularity,
            reverse = True
        )

        return Recommendations(
            name = 'New Populars for you',
            description = """
                Shuffle of most popular items non seen for session user.
                The idea is recommend new popular item, non seen for user in session.
                <br>
                Formula:
                <br>
                <strong>item_popularity = min_max_norm(mean(item_ratings) * min_max_norm(count(item_interactions)))</strong>
            """,
            items = selected_items
        )

