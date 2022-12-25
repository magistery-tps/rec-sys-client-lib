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
            id   = 'new_populars',
            name = 'New Populars for you',
            description = """
                <strong>Shuffle of user unrated popular items.</strong>
                The idea is recommend new popular items for you.
                <br>
                <br>
                Formula:
                <br>
                <strong>popularity = norm(mean(ratings) x norm(count(ratings)))</strong>
            """,
            items = selected_items
        )

