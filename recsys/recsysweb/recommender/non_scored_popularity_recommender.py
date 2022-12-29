from ..models               import Item, Recommendations, SimilarItemsResult
from .recommender           import Recommender
from .recommender_context   import RecommenderContext
from .recommender_metadata  import RecommenderMetadata

import random


class NonScoredPopularityRecommender(Recommender):
    @property
    def metadata(self):
        return RecommenderMetadata(
            id   = 1_000_000,
            name = 'New Populars For You',
            description = """
                <strong>Shuffle of user unrated popular items.</strong>
                The idea is recommend new popular items for you.
                <br>
                <br>
                Formula:
                <br>
                <strong>popularity = norm(mean(ratings) x norm(count(ratings)))</strong>
            """
        )

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
            metadata = self.metadata,
            items    = selected_items,
            info     = 'Not found recommendations!' if len(items) == 0 else ''
        )

    def find_similars(self, ctx: RecommenderContext):
        return SimilarItemsResult(self.metadata)
