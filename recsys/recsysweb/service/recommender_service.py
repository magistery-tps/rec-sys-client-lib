from django.core.exceptions import ObjectDoesNotExist
from ..models import Recommender, Interaction, ItemDetail
from ..recommender import   NonScoredPopularityRecommender, \
                            PopularityRecommender, \
                            CollaborativeFilteringRecommender, \
                            RecommenderContext
from .similarity_matrix_service import   SimilarityMatrixService


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


    def find_by(self, user, min_interactions=20):
        if self.n_interactions_by(user) < min_interactions:
            return self.__default_recommneders
        else:
            return self.__default_recommneders + \
                    [CollaborativeFilteringRecommender(r, self.similarity_matrix_service)  for r in Recommender.objects.all() if r.enable]


    def find_recommendations(self, user):
        recommenders = self.find_by(user)

        ctx = RecommenderContext(user=user)

        recommendations_list = [r.recommend(ctx) for r in recommenders]

        recommendations_list.sort(key=lambda r: r.position)

        return recommendations_list


    def find_recommender(self, recommender_id):
        try:
            return CollaborativeFilteringRecommender(
                Recommender.objects.get(id=recommender_id),
                self.similarity_matrix_service
            )
        except ObjectDoesNotExist as error:
            return self.__non_scored_popularity_recommender


    def find_item_detail(self, recommender, user, item):
        ctx = RecommenderContext(user=user, item=item)
        similar_items = recommender.find_similars(ctx)
        return ItemDetail(item, similar_items, recommender)