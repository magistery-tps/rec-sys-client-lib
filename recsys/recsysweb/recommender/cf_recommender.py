import random
from django.db.models import Q
from ..logger import get_logger
import numpy as np


# Domain
from ..models               import Item, Interaction, SimilarityMatrixCell, Recommendations, SimilarItemsResult
from .recommender           import Recommender
from .recommender_context   import RecommenderContext
from .recommender_metadata  import RecommenderMetadata
from .similar_item          import SimilarItem


class CollaborativeFilteringRecommender(Recommender):
    def __init__(self, config, similarity_matrix_service=None):
        self.__config = config
        self.logger = get_logger(self)
        self.similarity_matrix_service = similarity_matrix_service

    @property
    def metadata(self):
        return RecommenderMetadata(
            id          = self.__config.id,
            name        = self.__config.name,
            features    = f'{self.__config.name} | Similarity Matrix: {self.__config.user_similarity_matrix.name}, {self.__config.item_similarity_matrix.name}',
            title       = 'Other users also are reading',
            description = f"""<strong>Recommendation Strategy</strong><br>
                Use a collaborative filtering recommendation strategy based on <strong>{self.__config.name}</strong> model. 
                This recommender find items rated for similar users. To use these recommenders it's important to have a minimum number of rated items by user. 
                This recommenders have both user-to-user and item-to-item similarity matrix. user-to-user matrix is used to find a similar users list ordered by similarity. 
                Finally recommender looks for items rated by the users in it's list but not rated by current user in session.
                <br>
                <br>
                <strong>Item Similarity Strategy</strong><br>
                Use item-to-item similarity matrix to find item most similat to item into detail view. This similarity is influenced by user ratings. 
                On the other hand, also is possible assign external similarity matrix like matrix based into items content or any  similarity type.""",
            position    = self.__config.position
        )

    def recommend(self, ctx: RecommenderContext):
        most_similar_users = self.similarity_matrix_service \
            .find_similar_element_ids(
                matrix     = self.__config.user_similarity_matrix,
                element_id = ctx.user.id,
                limit      = self.__config.max_similar_users
            )

        most_similar_user_ids = most_similar_users.keys()

        mean_rating_by_non_seen_item_id = self.__non_seen_similar_user_items_mean_rating(ctx.user,most_similar_user_ids)

        recommended_items = Item.objects.filter(pk__in=mean_rating_by_non_seen_item_id.keys())

        recommended_items = sorted(
            recommended_items,
            key=lambda x: mean_rating_by_non_seen_item_id[x.id],
            reverse=True
        )[:ctx.limit]

        return self.__build_result(
            most_similar_user_ids,
            mean_rating_by_non_seen_item_id.keys(),
            recommended_items
        )


    def find_similars(self, ctx: RecommenderContext):
        most_similar_items = self.similarity_matrix_service \
            .find_similar_element_ids(
                matrix     = self.__config.item_similarity_matrix,
                element_id = ctx.item.id,
                limit      = self.__config.max_similar_items
            )

        recommended_items = Item.objects.filter(pk__in=most_similar_items.keys())

        recommended_items = [SimilarItem(item, most_similar_items[item.id]) for item in recommended_items]

        recommended_items = sorted(recommended_items, key=lambda x: x.similarity, reverse=True)

        self.logger.info([(i.id, i.similarity) for i in recommended_items])

        return SimilarItemsResult(self.metadata, recommended_items)



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
        info = 'At the moment there are no recommendations.' if len(recommended_items) == 0 else ''
        info += f' Found {len(most_similar_user_ids)} most similar users.'
        info += f' Found {len(non_seen_similar_user_item_ids)} non seen similar user items.'

        return Recommendations(
            metadata = self.metadata,
            items    = recommended_items,
            info     = info
        )
