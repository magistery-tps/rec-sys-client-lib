from ..models import Item, Interaction, SimilarityMatrix, SimilarityMatrixCell, Recommendations
from .recommender import Recommender, RecommenderContext
import random


class CollaborativeFilteringRecommender(Recommender):
    def __init__(self, recommender_data):
        self.__recommender_data = recommender_data


    def __similar_user_ids(self, user):
        user_sim_matrix = self.__recommender_data.user_similarity_matrix

        sim_cells = SimilarityMatrixCell.objects.filter(
            row     = user.id,
            matrix  = user_sim_matrix.id,
            version = user_sim_matrix.version
        ).order_by('-value')

        return [c.column for c in sim_cells]


    def recommend(self, ctx: RecommenderContext):
        similar_user_ids = self.__similar_user_ids(ctx.user)

        similar_users_interactions = Interaction \
            .objects \
            .filter(user__in=similar_user_ids)

        item_ids = [interaction.item_id for interaction in similar_users_interactions]

        items = Item.objects.filter(pk__in=item_ids).order_by('-popularity')[:ctx.shuffle_limit]

        if len(items) > 0:
            items = random.sample(list(items), ctx.limit)

        info = 'Not found recommendations!' if len(items) == 0 else ''
        info += f' Found {len(similar_user_ids)} similar users.'
        info += f' Found {len(item_ids)} similar user items.'

        return Recommendations(
            id          = self.__recommender_data.name,
            name        = f'{self.__recommender_data.name}: Other users are also reading',
            description = f'<strong>{self.__recommender_data.name}</strong> collaborative filtering recommender. This recommender find items rated for similar users. Is required count with a minimum number of items rated for use these recommenders.',
            items       = items,
            info        = info
        )
