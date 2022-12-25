from ..models import Item, SimilarityMatrix, SimilarityMatrixCell, Recommendations
from .recommender import Recommender, RecommenderContext
import random


class CollaborativeFilteringRecommender(Recommender):
    def __init__(self, recommender_data):
        self.__recommender_data = recommender_data


    def recommend(self, ctx: RecommenderContext):
        items = Item.objects.all().order_by('-popularity')[ctx.shuffle_limit:]

        selected_items = random.sample(list(items), ctx.limit)

        selected_items = sorted(
            selected_items,
            key     = lambda item: item.popularity,
            reverse = True
        )

        return Recommendations(
            name        = f'{self.__recommender_data.name}: Other users are also reading',
            description = f"""
                <strong>{self.__recommender_data.name}</strong> collaborative filtering recommender.
            """,
            items       = selected_items
        )