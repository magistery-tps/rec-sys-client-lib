from django.db import models
from .recommender_ensemble  import RecommenderEnsemble


class RecommenderEnsempleEvaluation(models.Model):
    id          = models.AutoField(primary_key=True)
    enable      = models.BooleanField(default = True, verbose_name = 'Enable')
    ensemble    = models.ForeignKey(
        RecommenderEnsemble,
        db_column    = 'ensemble_id',
        related_name ='%(class)s_ensemble_id',
        on_delete    = models.DO_NOTHING,
        unique       = True,
        verbose_name = 'Recommender Ensemble'
    )

    class Meta:
        indexes = [
            models.Index(fields=['enable']),
            models.Index(fields=['enable', 'ensemble'])
        ]


    def __str__(self):
        return f'{self.ensemble.name} Evaluation'