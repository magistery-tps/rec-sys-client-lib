import random
from django.db.models import Q
from ..logger import get_logger
import numpy as np


# Domain
from ..models       import Item, Interaction, SimilarityMatrixCell, Recommendations
from .recommender   import Recommender, RecommenderContext, RecommenderMetadata


class CollaborativeFilteringRecommender(Recommender):
    def __init__(self, config, simialrity_matrix_service=None):
        self.__config = config
        self.logger = get_logger(self)
        self.simialrity_matrix_service = simialrity_matrix_service

    @property
    def metadata(self):
        return RecommenderMetadata(
            id         = self.__config.id,
            name       = self.__config.name,
            description = f'<strong>{self.__config.name}</strong> collaborative filtering recommender. This recommender find items rated for similar users. Is required count with a minimum number of items rated for use these recommenders.',
            position    = self.__config.position
        )

    def recommend(self, ctx: RecommenderContext):
        most_similar_user_ids = self.simialrity_matrix_service \
            .find_similar_element_ids(
                matrix     = self.__config.user_similarity_matrix,
                element_id = ctx.user.id,
                limit      = self.__config.max_similar_users
            )

        mean_rating_by_non_seen_item_id = self.__non_seen_similar_user_items_mean_rating(ctx.user, most_similar_user_ids)

        recommended_items = Item.objects.filter(pk__in=mean_rating_by_non_seen_item_id.keys())


        recommended_items = sorted(
            recommended_items,
            key=lambda x: mean_rating_by_non_seen_item_id[x.id],
            reverse=True
        )
        recommended_items = recommended_items[:ctx.limit]

        # self.logger.info('\n\nRESULT:\n')
        # for i in recommended_items:
        #   self.logger.info(f'{i.name}: {mean_rating_by_non_seen_item_id[i.id]}')

        return self.__build_result(most_similar_user_ids, mean_rating_by_non_seen_item_id.keys(), recommended_items)


    def find_similars(self, ctx: RecommenderContext):
        most_similar_item_ids = self.simialrity_matrix_service \
            .find_similar_element_ids(
                matrix     = self.__config.item_similarity_matrix,
                element_id = ctx.item.id,
                limit      = self.__config.max_similar_items
            )


        recommended_items = Item.objects.filter(pk__in=most_similar_item_ids)

        recommended_items= sorted(
            recommended_items,
            key=lambda x: most_similar_item_ids.index(x.id)
        )

        self.logger.info([i.id for i in recommended_items])

        return recommended_items



    def __non_seen_similar_user_items_mean_rating(self, user, similar_user_ids):
        user_item_ids = [item.item_id for item in Interaction.objects.filter(user=user.id)]


        similar_user_interactions = []
        for similar_user_id in similar_user_ids:
            similar_user_interactions.extend(Interaction.objects.filter(user=similar_user_id)[:self.__config.max_items_by_similar_user])

        rating_by_item_id = {}
        for i in similar_user_interactions:
            if i.item_id not in user_item_ids:
                if i.item_id in rating_by_item_id:
                    rating_by_item_id[i.item_id].append(i.rating)
                else:
                    rating_by_item_id[i.item_id] = [i.rating]

        mean_rating_by_item_id = {id: np.mean(ratings) for id, ratings in rating_by_item_id.items()}

        return mean_rating_by_item_id


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
            metadata = self.metadata,
            items    = recommended_items,
            info     = info
        )
