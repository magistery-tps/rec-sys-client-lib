from ..models import Item, Interaction, SimilarityMatrix, SimilarityMatrixCell, Recommendations
from .recommender import Recommender, RecommenderContext
import random
from ..logger import get_logger


class CollaborativeFilteringRecommender(Recommender):
    def __init__(self, recommender_data):
        self.__recommender_data = recommender_data
        self.logger = get_logger(self)


    def __similar_user_ids(self, user):
        user_sim_matrix = self.__recommender_data.user_similarity_matrix

        sim_cells = SimilarityMatrixCell.objects.filter(
            row     = user.id,
            matrix  = user_sim_matrix.id,
            version = user_sim_matrix.version
        ).order_by('-value')

        return [c.user.id for c in sim_cells]


    def recommend(self, ctx: RecommenderContext):
        similar_user_ids = self.__similar_user_ids(ctx.user)
        self.logger.info(f'similar_user_ids: {len(similar_user_ids)}')


        similar_users_interactions = Interaction \
            .objects \
            .filter(user__in=similar_user_ids)

        item_ids = set([item.id for item in similar_users_interactions])

        items    = Item.objects.filter(pk__in=list(item_ids))

        items = sorted(
            items,
            key     = lambda item: item.popularity,
            reverse = True
        )

        not_found = 'Not found recommendations!'
        if len(similar_user_ids) == 0:
            not_found += ' Not found similar users.'
        if len(item_ids) == 0:
            not_found += ' Not found similar user items.'

        return Recommendations(
            id          = self.__recommender_data.name,
            name        = f'{self.__recommender_data.name}: Other users are also reading',
            description = f'<strong>{self.__recommender_data.name}</strong> collaborative filtering recommender. This recommender find items rated for similar users. Is required count with a minimum number of items rated for use these recommenders.',
            items       = items,
            not_found   = not_found
        )
