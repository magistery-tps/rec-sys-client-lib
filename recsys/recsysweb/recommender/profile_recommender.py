from ..models               import Item, Recommendations, SimilarItemsResult
from .recommender           import Recommender
from .recommender_context   import RecommenderContext
from .recommender_metadata  import RecommenderMetadata
import random
import numpy as np


class ProfileRecommender(Recommender):
    def __init__(self, tag_service):
        self.__tag_service = tag_service

    @property
    def metadata(self):
        return RecommenderMetadata(
            id   = 3_000_000,
            name = 'tags_profile',
            features = 'Recommender: User Tags Profile, Similars: Rank By Shared Tags',
            title = 'Similars by Rated Tags',
            description = """
                <strong>Recommender Startegy</strong><br>
                Build a tags probability distribution only for items rated by current user.
                When order items descendent by this score. It recommend items based on rated tags frequency.
                This recommender suffer of tunnel effect. Users only see items with similar tags,
                but can't discover more relevant item with other tags.
                <br>
                <strong>Similars Startegy</strong><br>
                Returns other items tagged similarly to current/detaled item, ordered with most similar first.
                The more tags items have in common, the more similar they are.
            """
        )

    def recommend(self, ctx: RecommenderContext):
        user_profile = self.__tag_service.find_user_profile_by(ctx.user)

        score_by_id = { profile.id: profile.score  for profile in user_profile }

        items = set(Item.objects.filter(tags__id__in = score_by_id.keys(), popularity__gt = 0.2))

        scored_items = []
        for item in items:
            mean_score = np.mean([score_by_id.get(tag['id'], 0) for tag in item.tags.values()])
            scored_items.append((item, mean_score))

        scored_items = sorted(scored_items, key=lambda item: item[1], reverse=True)

        return Recommendations(
            metadata = self.metadata,
            items    = [item[0] for item in scored_items[:ctx.limit]],
            info     = 'Not found recommendations!' if len(items) == 0 else ''
        )

    def find_similars(self, ctx: RecommenderContext):
        similar_items = ctx.item.tags.similar_objects()[:10]
        return SimilarItemsResult(self.metadata, similar_items)