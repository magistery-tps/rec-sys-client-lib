from django.core.exceptions import ObjectDoesNotExist
from ..models import Recommender, Interaction, ItemDetail, SimilarItemsResult
from ..recommender import   NonScoredPopularityRecommender, \
                            PopularityRecommender, \
                            CollaborativeFilteringRecommender, \
                            RecommenderContext
from .similarity_matrix_service import   SimilarityMatrixService
import logging

class RecommenderService:
    def __init__(self):
        self.__non_scored_popularity_recommender = NonScoredPopularityRecommender()
        self.__default_recommneders = [
            PopularityRecommender(),
            self.__non_scored_popularity_recommender
        ]
        self.similarity_matrix_service = SimilarityMatrixService()


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
        recommenders = self.find_by_user(user)

        ctx = RecommenderContext(user=user)

        recommendations_list = [r.recommend(ctx) for r in recommenders]

        recommendations_list.sort(key=lambda r: r.position)

        return recommendations_list


    def find_item_detail(self, recommenders, item):
        ctx = RecommenderContext(item=item)
        results = []
        for rec in recommenders:
            similar_items = rec.find_similars(ctx)
            if len(similar_items) > 0:
                logging.info(rec.metadata.name)
                results.append(SimilarItemsResult(rec.metadata, similar_items))

        return ItemDetail(item, results)