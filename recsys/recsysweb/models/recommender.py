from django.db          import models
from .similarity_matrix import SimilarityMatrix


class Recommender(models.Model):
    id          = models.AutoField(primary_key=True)
    name        = models.CharField(
        max_length   = 200,
        verbose_name = 'Name',
        unique       = True
    )
    user_similarity_matrix = models.ForeignKey(
        SimilarityMatrix,
        db_column    = 'user_similarity_matrix_id',
        related_name ='%(class)s_user_similarity_matrix_id',
        on_delete    = models.DO_NOTHING,
        unique       = False,
        verbose_name = 'User Similarity Matrix'
    )
    item_similarity_matrix = models.ForeignKey(
        SimilarityMatrix,
        db_column    = 'item_similarity_matrix_id',
        related_name ='%(class)s_item_similarity_matrix_id',
        on_delete    = models.DO_NOTHING,
        unique       = False,
        verbose_name = 'Item Similarity Matrix'
    )


    def __str__(self):
        return f'Name: {self.name}'
