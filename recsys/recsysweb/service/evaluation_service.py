from ..models import RecommenderEnsempleEvaluation
from singleton_decorator import singleton
from django.db.models import Avg


@singleton
class EvaluationService:
    def find_active(self):
        return RecommenderEnsempleEvaluation.objects.filter(enable=True)[0]


    def find_metric_by_active_and_user(self, user):
        evaluation = self.find_active(self)
        return RecommenderEnsempleEvaluation \
            .objects \
            .filter(evaluation=evaluation, user=user) \
            .aggregate(Avg('value'))


    def find_metric_by_active(self):
        evaluation = self.find_active(self)
        return RecommenderEnsempleEvaluation \
            .objects \
            .filter(evaluation=evaluation) \
            .aggregate(Avg('value'))

