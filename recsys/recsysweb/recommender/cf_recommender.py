from ..models import Item, Interaction, SimilarityMatrix, SimilarityMatrixCell, Recommendations
from .recommender import Recommender, RecommenderContext
import random
from django.db.models import Q

class CollaborativeFilteringRecommender(Recommender):
    def __init__(self, recommender_data):
        self.__recommender_data = recommender_data


    def __similar_user_ids(self, user):
        user_sim_matrix = self.__recommender_data.user_similarity_matrix

        similar_user_ids = []

        sim_cells = SimilarityMatrixCell.objects.filter(
            row       = user.id,
            matrix    = user_sim_matrix.id,
            version   = user_sim_matrix.version,
            value__gt = 0
        ).order_by('-value')
        if len(sim_cells) > 0:
            similar_user_ids.extend([c.column for c in sim_cells])

        sim_cells = SimilarityMatrixCell.objects.filter(
            column  = user.id,
            matrix  = user_sim_matrix.id,
            version = user_sim_matrix.version,
            value__gt = 0
        ).order_by('-value')

        similar_user_ids.extend([c.row for c in sim_cells])

        return set(similar_user_ids)


    def __get_user_items(self, user):
        items = Interaction.objects.filter(user=user.id)
        return [i.item_id for i in items]


    def recommend(self, ctx: RecommenderContext):
        similar_user_ids = self.__similar_user_ids(ctx.user)

        own_item_ids = self.__get_user_items(ctx.user)

        similar_users_interactions = Interaction \
            .objects \
            .filter(user__in=similar_user_ids)
        similar_users_item_ids = set([i.item_id for i in similar_users_interactions if i.item_id not in own_item_ids])

        items = Item.objects.filter(pk__in=similar_users_item_ids).order_by('-popularity')[:ctx.limit]

        info = 'Not found recommendations!' if len(items) == 0 else ''
        info += f' Found {len(similar_user_ids)} similar users.'
        info += f' Found {len(similar_users_item_ids)} similar user items.'

        return Recommendations(
            id          = self.__recommender_data.name,
            name        = f'{self.__recommender_data.name}: Other users are also reading',
            description = f'<strong>{self.__recommender_data.name}</strong> collaborative filtering recommender. This recommender find items rated for similar users. Is required count with a minimum number of items rated for use these recommenders.',
            items       = items,
            info        = info
        )
