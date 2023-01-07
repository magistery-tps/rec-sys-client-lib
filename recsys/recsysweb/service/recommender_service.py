from django.core.exceptions     import  ObjectDoesNotExist
from ..models                   import  Recommender, RecommenderEnsemble, RecommenderType, ItemDetail
from ..recommender              import  RecommenderContext, RecommenderFactory, RecommenderCapability
from .interaction_service       import  InteractionService
from .similarity_matrix_service import  SimilarityMatrixService
from .tag_service               import  TagService
from .item_service              import  ItemService
import logging
from singleton_decorator import singleton


@singleton
class RecommenderService:
    def __init__(self):
        item_service                = ItemService()
        tag_service                 = TagService()
        self.__interaction_service  = InteractionService()
        similarity_matrix_service   = SimilarityMatrixService()
        self.__recommender_factory  = RecommenderFactory(
            self.__interaction_service,
            item_service,
            tag_service,
            similarity_matrix_service
        )

    def find_items_non_scored_by(self, user):
        config = Recommender.objects.get(type=RecommenderType.NEW_POPULARS)
        recommender = self.__recommender_factory.create(config)
        return recommender.recommend(ctx = RecommenderContext(user=user))


    def find_by_user(self, user, min_interactions=20):
        if self.__interaction_service.count_by_user(user) < min_interactions:
            configs = Recommender.objects.filter(
                type_in=[
                    RecommenderType.POPULARS,
                    RecommenderType.NEW_POPULARS,
                    RecommenderType.USER_PROFILE
                ],
                enable=True
            )
            recommenders = [self.__recommender_factory.create(c) for c in configs]
        else:
            configs = RecommenderEnsemble.objects.all()
            recommenders = [self.__recommender_factory.create(c) for c in configs]

            configs = Recommender.objects.filter(enable=True)
            recommenders.extend([self.__recommender_factory.create(c) for c in configs])
            return recommenders


    def find_by_id(self, id):
        try:
            return self.__recommender_factory.create(
                config = Recommender.objects.get(id=id)
            )
        except ObjectDoesNotExist as error:
            try:
                return self.__recommender_factory.create(
                    config = RecommenderEnsemble.objects.get(id=id)
                )
            except ObjectDoesNotExist as error:
                return None


    def find_by_user_recommender_id_and_capability(self, user, id, capability):
        recommender = self.find_by_id(id)

        if RecommenderCapability.SIMILARS in recommender.capabilities:
            return [recommender]
        else:
            recommenders = self.find_by_user(user)
            return [r for r in recommenders if RecommenderCapability.SIMILARS in r.capabilities]


    def find_recommendations(self, user):
        ctx = RecommenderContext(user=user)
        return sorted([r.recommend(ctx) for r in self.find_by_user(user)], key=lambda r: r.position)


    def find_item_detail(self, recommenders, item, user):
        ctx = RecommenderContext(item=item, user=user)
        recommenders = sorted(recommenders, key=lambda x: x.metadata.position)
        return ItemDetail(item, [rec.find_similars(ctx) for rec in recommenders])