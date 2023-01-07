from django.db              import models
from .recommender           import Recommender
from .recommender_ensemble  import RecommenderEnsemble


class RecommenderEnsembleConfig(models.Model):
    id          = models.AutoField(primary_key=True)
    ensemble    = models.ForeignKey(
        RecommenderEnsemble,
        db_column    = 'ensemble_id',
        related_name ='%(class)s_ensemble_id',
        on_delete    = models.DO_NOTHING,
        unique       = False,
        verbose_name = 'Recommender Ensemble'
    )
    recommender = models.ForeignKey(
        Recommender,
        db_column    = 'recommender_id',
        related_name ='%(class)s_recommender_id',
        on_delete    = models.DO_NOTHING,
        unique       = False,
        verbose_name = 'Recommender'
    )
    active_from_n_user_iterations = models.IntegerField(default = 0, verbose_name = 'Active from n user interactions')
    active_to_n_user_iterations   = models.IntegerField(default = 0, verbose_name = 'Active to n user interactions')
