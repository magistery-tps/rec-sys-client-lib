from ..models import Recommender, Interaction
from ..recommender import   NonScoredPopularityRecommender, \
                            PopularityRecommender, \
                            CollaborativeFilteringRecommender, \
                            RecommenderContext


class RecommenderService:
    def __init__(self):
        self.__default_recommneders = [PopularityRecommender(), NonScoredPopularityRecommender()]


    def __n_interactions_by(self, user):
        return Interaction.objects.filter(user=user.id).count()


    def find_by(self, user, min_interactions=20):
        if self.__n_interactions_by(user) < min_interactions:
            return self.__default_recommneders
        else:
            return self.__default_recommneders + \
                    [CollaborativeFilteringRecommender(r)  for r in Recommender.objects.all()]


    def find_recommendations(self, user):
        recommenders = self.find_by(user)

        ctx = RecommenderContext(user=user)

        recommendations_list = [r.recommend(ctx) for r in recommenders]

        return [r for r in recommendations_list if not r.empty]
