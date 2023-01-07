from django.db          import models
from .similarity_matrix import SimilarityMatrix


class RecommenderEnsemble(models.Model):
    id          = models.AutoField(primary_key=True)
    name        = models.CharField(
        max_length   = 200,
        verbose_name = 'Name',
        unique       = True
    )
    description = models.TextField(
        max_length   = 5000,
        verbose_name = 'Description',
        default      = ''
    )
    position = models.IntegerField(default = 1, verbose_name = 'Position in Recommendations View')
    enable = models.BooleanField(default = True, verbose_name = 'Enable')

    def __str__(self):
        return self.name