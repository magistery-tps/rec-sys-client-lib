from ..models import Recommender, Interaction
from ..recommender import   NonScoredPopularityRecommender, \
                            PopularityRecommender, \
                            CollaborativeFilteringRecommender, \
                            RecommenderContext


class RecommenderService:
    def __init__(self):
        self.__non_scored_popularity_recommender = NonScoredPopularityRecommender()
        self.__default_recommneders = [
            PopularityRecommender(),
            self.__non_scored_popularity_recommender
        ]


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
                    [CollaborativeFilteringRecommender(r)  for r in Recommender.objects.all()]


    def find_recommendations(self, user):
        recommenders = self.find_by(user)

        ctx = RecommenderContext(user=user)

        recommendations_list = [r.recommend(ctx) for r in recommenders]

        return [r for r in recommendations_list if not r.empty]
