from ..models                   import Recommendations, SimilarItemsResult
from .recommender               import Recommender
from .recommender_context       import RecommenderContext
from .recommender_metadata      import RecommenderMetadata
from .recommender_capability    import RecommenderCapability
import numpy as np


class ProfileRecommender(Recommender):
    def __init__(self, config, tag_service, item_service):
        super().__init__(config)
        self.__tag_service  = tag_service
        self.__item_service = item_service


    @property
    def metadata(self):
        return RecommenderMetadata(
            id          = self.config.id,
            name        = f'recommender-{self.config.id}',
            features    = 'User Tags Profile',
            title       = self.config.name,
            description = self.config.description,
            position    = self.config.position
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


    @property
    def capabilities(self):
        return [RecommenderCapability.RECOMMEND, RecommenderCapability.SIMILARS]