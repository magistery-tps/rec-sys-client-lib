from django.db import models


class RecommenderType(models.IntegerChoices):
    POPULARS                = 1
    NEW_POPULARS            = 2
    COLLAVORATIVE_FILTERING = 3
    USER_PROFILE            = 4
