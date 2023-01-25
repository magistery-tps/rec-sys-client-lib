from django.db import models
from .recommender_esemble_evaluation import RecommenderEnsempleEvaluation
from django.contrib.auth.models import User
from datetime import datetime


class RecommenderEnsempleEvaluationMetric(models.Model):
    id          = models.AutoField(primary_key=True)
    evaluation  = models.ForeignKey(
        RecommenderEnsempleEvaluation,
        db_column    = 'evaluation_id',
        related_name ='%(class)s_evaluation_id',
        on_delete    = models.CASCADE,
        unique       = False,
        verbose_name = 'Recommender Ensemble Evaluation'
    )
    user        = models.ForeignKey(
        User,
        db_column    = 'user_id',
        related_name ='%(class)s_user_id',
        on_delete    = models.DO_NOTHING,
        unique       = False,
        verbose_name = 'User'
    )
    value       = models.FloatField()
    datetime    = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['evaluation', 'user']),
            models.Index(fields=['evaluation']),
            models.Index(fields=['user'])
        ]
