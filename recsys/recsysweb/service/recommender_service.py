from django.core.exceptions import ObjectDoesNotExist
from ..models import Recommender, Interaction, ItemDetail
from ..recommender import (
    NonScoredPopularityRecommender,
    PopularityRecommender,
    CollaborativeFilteringRecommender,
    RecommenderContext,
    ProfileRecommender
)
from .similarity_matrix_service import  SimilarityMatrixService
from .tag_service               import  TagService
from .item_service              import  ItemService
import logging


class RecommenderService:
    def __init__(self):
        tag_service                     = TagService()
        item_service                    = ItemService()
        self.similarity_matrix_service  = SimilarityMatrixService()

        profile_recommender                      = ProfileRecommender(tag_service, item_service)
        popularity_recommender                   = PopularityRecommender(item_service)
        self.__non_scored_popularity_recommender = NonScoredPopularityRecommender(item_service)

        self.__default_recommneders = [
            popularity_recommender,
            self.__non_scored_popularity_recommender,
            profile_recommender
        ]


    def n_interactions_by(self, user):
        return Interaction.objects.filter(user=user.id).count()


    def find_items_non_scored_by(self, user):
        ctx = RecommenderContext(user=user)
        return self.__non_scored_popularity_recommender.recommend(ctx)


    def find_by_user(self, user, min_interactions=20):
        if self.n_interactions_by(user) < min_interactions:
            return self.__default_recommneders
        else:
            return self.__default_recommneders + \
                    [CollaborativeFilteringRecommender(r, self.similarity_matrix_service)  for r in Recommender.objects.all() if r.enable]


    def find_by_id(self, recommender_id):
        try:
            return CollaborativeFilteringRecommender(
                Recommender.objects.get(id=recommender_id),
                self.similarity_matrix_service
            )
        except ObjectDoesNotExist as error:
            return None


    def find_recommendations(self, user):
        ctx = RecommenderContext(user=user)
        return sorted([r.recommend(ctx) for r in self.find_by_user(user)], key=lambda r: r.position)


    def find_item_detail(self, recommenders, item):
        ctx = RecommenderContext(item=item)
        recommenders = sorted(recommenders, key=lambda x: x.metadata.position)
        return ItemDetail(item, [rec.find_similars(ctx) for rec in recommenders])