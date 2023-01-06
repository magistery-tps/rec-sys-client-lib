from ..models               import Recommendations, SimilarItemsResult
from .recommender           import Recommender
from .recommender_context   import RecommenderContext
from .recommender_metadata  import RecommenderMetadata
import numpy as np


class ProfileRecommender(Recommender):
    def __init__(self, tag_service, item_service):
        self.__tag_service  = tag_service
        self.__item_service = item_service

    @property
    def metadata(self):
        return RecommenderMetadata(
            id   = 3_000_000,
            name = 'tags_profile',
            features = 'User Tags Profile | Similarity: Tags based',
            title = 'New Similars by Rated Tags',
            description = """
                <strong>Recommender Startegy</strong><br>
                Build a tags probability distribution only for items rated by current user.
                When order items descendent by this score. It recommend items based on rated tags frequency.
                This recommender suffer of tunnel effect. Users only see items with similar tags,
                but can't discover more relevant item with other tags.
                <br>
                <strong>Similars Strategy</strong><br>
                Returns other items tagged similarly to current/detaled item, ordered with most similar first.
                The more tags items have in common, the more similar they are.
            """
        )

    def recommend(self, ctx: RecommenderContext):
        user_item_ids = self.__item_service.find_ids_by_user(ctx.user)

        user_profile  = self.__tag_service.find_user_profile_by(user_item_ids)

        score_by_id = { profile.id: profile.score  for profile in user_profile }

        user_unrated_items = self.__item_service.find_complement_by_tags(
            item_ids        = user_item_ids,
            tag_ids         = score_by_id.keys(),
            min_popularity  = 0.2
        )

        mean_score = lambda item: np.mean([score_by_id.get(tag['id'], 0) for tag in item.tags.values()])

        scored_user_unrated_items = [(item, mean_score(item)) for item in user_unrated_items]

        scored_user_unrated_items = sorted(scored_user_unrated_items, key=lambda item: item[1], reverse=True)

        return Recommendations(
            metadata = self.metadata,
            items    = [item[0] for item in scored_user_unrated_items[:ctx.limit]],
            info     = 'At the moment there are no recommendations. Must rate at least 3 items to see good recommendations!' if len(scored_user_unrated_items) == 0 else ''
        )

    def find_similars(self, ctx: RecommenderContext):
        similar_items = ctx.item.tags.similar_objects()[:10]
        return SimilarItemsResult(self.metadata, similar_items)
