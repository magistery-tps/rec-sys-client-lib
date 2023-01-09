from ..models import RecommenderEnsempleEvaluation, RecommenderEnsempleEvaluationMetric
from singleton_decorator import singleton
from django.db.models import Avg
import math
import statistics


class Metrics:
    @staticmethod
    def normalized_discount_cumulative_gain(user_ratings):
        dcg = 0
        idcg = 0

        groud_truth = sorted(user_ratings, reverse=True)

        for i, r in enumerate(user_ratings):
            rel = int(r in groud_truth)
            dcg += rel / math.log2(i+1+1)
            idcg += groud_truth[i] / math.log2(i+1+1)

        return dcg / idcg if idcg else 0


@singleton
class EvaluationService:
    def find_active(self):
        return RecommenderEnsempleEvaluation.objects.filter(enable=True)[0]


    def find_metric_by_active_and_user(self, user):
        evaluation = self.find_active()
        return RecommenderEnsempleEvaluationMetric \
            .objects \
            .filter(evaluation=evaluation, user=user) \
            .aggregate(Avg('value')) \
            .get('value__avg', 0)


    def find_metric_by_active(self):
        evaluation = self.find_active()
        return RecommenderEnsempleEvaluationMetric \
            .objects \
            .filter(evaluation=evaluation) \
            .aggregate(Avg('value')) \
            .get('value__avg', 0)


    def evaluate_session(self, user, items_rating):
        discount_cumulative_gain = Metrics.normalized_discount_cumulative_gain(items_rating.values())

        evaluation = self.find_active()

        mertic = RecommenderEnsempleEvaluationMetric(
            evaluation = evaluation,
            user       = user,
            value      = discount_cumulative_gain
        )
        mertic.save()

    def remove_metrics_by_user(self, user):
        RecommenderEnsempleEvaluationMetric.objects.filter(user=user).delete()
