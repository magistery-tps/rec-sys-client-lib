from django.core.exceptions     import  ObjectDoesNotExist
from ..models                   import  Recommender, RecommenderEnsemble, RecommenderType, ItemDetail
from ..recommender              import  RecommenderContext, RecommenderFactory, RecommenderCapability
import logging
from singleton_decorator import singleton


@singleton
class RecommenderService:
    def __init__(self, ctx): self.ctx = ctx


    def find_by_user(self, user, min_interactions=20):
        if self.ctx.interaction_service.count_by_user(user) < min_interactions:
            try:
                configs = Recommender.objects.filter(
                    type__in=[
                        RecommenderType.POPULARS,
                        RecommenderType.NEW_POPULARS,
                        RecommenderType.USER_PROFILE
                    ],
                    enable=True
                )
                return [self.ctx.recommender_factory.create(c) for c in configs]
            except ObjectDoesNotExist as error:
                raise Error(f'Not found recommender/ensemble by id: {id}. {error}')
        else:
            configs = RecommenderEnsemble.objects.all()
            recommenders = [self.ctx.recommender_factory.create(c) for c in configs]
            try:
                configs = Recommender.objects.filter(enable=True)
                recommenders.extend([self.ctx.recommender_factory.create(c) for c in configs])
                return recommenders
            except ObjectDoesNotExist as error:
                raise Error(f'Not found enable recommenders. {error}')


    def find_by_id(self, id):
        try:
            return self.ctx.recommender_factory.create(
                config = Recommender.objects.get(id=id)
            )
        except ObjectDoesNotExist as error:
            try:
                return self.ctx.recommender_factory.create(
                    config = RecommenderEnsemble.objects.get(id=id)
                )
            except ObjectDoesNotExist as error:
                raise Error(f'Not found recommender/ensemble by id: {id}. {error}')


    def find_by_user_recommender_id_and_capability(self, user, id, capability):
        recommender = self.find_by_id(id)

        if recommender and RecommenderCapability.SIMILARS in recommender.capabilities:
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


    def find_recommendations_from_active_evaluation(self, user):
        evaluation  = self.ctx.evaluation_service.find_active()
        recommender = self.find_by_id(evaluation.ensemble.id)
        return recommender.recommend(ctx = RecommenderContext(user=user))