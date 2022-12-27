from ..models import Item, Interaction, SimilarityMatrix, SimilarityMatrixCell, Recommendations
from .recommender import Recommender, RecommenderContext
import random
from django.db.models import Q
from ..logger import get_logger

class CollaborativeFilteringRecommender(Recommender):
    def __init__(self, config):
        self.__config = config
        self.logger = get_logger(self)


    def __similar_user_ids(self, user):
        user_sim_matrix = self.__config.user_similarity_matrix


        similar_col_cells = SimilarityMatrixCell.objects.filter(
            row       = user.id,
            matrix    = user_sim_matrix.id,
            version   = user_sim_matrix.version,
            value__gt = 0
        ).order_by('-value')

        sim_by_id = { cell.column: cell.value for cell in similar_col_cells }


        similar_row_cels = SimilarityMatrixCell.objects.filter(
            column  = user.id,
            matrix  = user_sim_matrix.id,
            version = user_sim_matrix.version,
            value__gt = 0
        ).order_by('-value')


        for cell in similar_row_cels:
            if cell.row in sim_by_id and cell.value < sim_by_id[cell.row]:
                sim_by_id[cell.row] = cell.value
            else:
                sim_by_id[cell.row] = cell.value


        id_sim_list =  list(sim_by_id.items())
        id_sim_list.sort(key=lambda id_sim: id_sim[1], reverse=True)


        return [id_sim[0] for id_sim in id_sim_list]


    def __non_seen_similar_user_item_ids(self, user, similar_user_ids):
        user_item_ids = [item.item_id for item in Interaction.objects.filter(user=user.id)]

        similar_user_interactions = []
        for similar_user_id in similar_user_ids:
            similar_user_interactions.extend(Interaction.objects.filter(user=similar_user_id)[:self.__config.max_items_by_similar_user])

        return set([item.item_id for item in similar_user_interactions if item.item_id not in user_item_ids])


    def recommend(self, ctx: RecommenderContext):
        most_similar_user_ids = self.__similar_user_ids(ctx.user)[:self.__config.max_similar_users]

        non_seen_similar_user_item_ids = self.__non_seen_similar_user_item_ids(ctx.user, most_similar_user_ids)

        recommended_items = Item.objects.filter(pk__in=non_seen_similar_user_item_ids).order_by('-popularity')[:ctx.limit]

        for i in recommended_items:
            self.logger.info(i)

        return self.__build_result(most_similar_user_ids, non_seen_similar_user_item_ids, recommended_items)


    def __build_result(
        self,
        most_similar_user_ids,
        non_seen_similar_user_item_ids,
        recommended_items
    ):
        info = 'Not found recommendations!' if len(recommended_items) == 0 else ''
        info += f' Found {len(most_similar_user_ids)} most similar users.'
        info += f' Found {len(non_seen_similar_user_item_ids)} non seen similar user items.'

        return Recommendations(
            id          = str(self.__config.id),
            name        = f'{self.__config.max_similar_users} Most Similar Users Are Also Reading ({self.__config.name} Recommender)',
            description = f'<strong>{self.__config.name}</strong> collaborative filtering recommender. This recommender find items rated for similar users. Is required count with a minimum number of items rated for use these recommenders.',
            items       = recommended_items,
            info        = info,
            position    = self.__config.position
        )
