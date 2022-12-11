from django.db import models


class SimilarityMatrixType(models.IntegerChoices):
    USER_TO_USER = 1
    ITEM_TO_ITEM = 2
