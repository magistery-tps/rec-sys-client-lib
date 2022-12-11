from django.db          import models
from .similarity_matrix import SimilarityMatrix


class SimilarityMatrixCell(models.Model):
    row    = models.IntegerField(db_column='row')
    column = models.IntegerField(db_column='column')
    matrix = models.ForeignKey(
        SimilarityMatrix,
        db_column  = 'similarity_matrix_id',
        on_delete  = models.DO_NOTHING,
        unique     = False
    )
    value = models.FloatField()

    def __str__(self):
        return f'row: {self.row} | Column: {self.column} | Value: {self.value} | Matrix: {self.matrix}'
