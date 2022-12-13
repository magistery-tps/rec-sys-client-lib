from django.db               import models
from .similarity_matrix_type import SimilarityMatrixType


class SimilarityMatrix(models.Model):
    id          = models.AutoField(primary_key=True)
    type        = models.IntegerField(
        choices = SimilarityMatrixType.choices,
        default = SimilarityMatrixType.USER_TO_USER
    )
    name        = models.CharField(
        max_length   = 200,
        verbose_name = 'Name',
        unique       = True
    )
    description = models.TextField(
        max_length   = 1000,
        verbose_name = 'Description'
    )
    version = models.IntegerField(default=0)

    def __str__(self):
        return f'Type: {self.type} | Name: {self.name} | Desc: {self.description}'

