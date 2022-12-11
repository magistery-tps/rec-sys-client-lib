from django.db import models
from .item     import Item


class Interaction(models.Model):
# ------------------------------------------------------------
# Note:
# ------------------------------------------------------------
#   Not used. Because 99% of users are used to have a base to
#   predict ratings. Threare a 1% of real users.
# ------------------------------------------------------------
#    user = models.ForeignKey(
#        'auth.User',
#        db_column  = 'user_id',
#        on_delete  = models.DO_NOTHING,
#        unique     = False
#   )
# ------------------------------------------------------------
    user    = models.IntegerField(
        db_column  = 'user_id',
        unique     = False
    )
    item    = models.ForeignKey(
        Item,
        db_column  = 'item_id',
        on_delete  = models.DO_NOTHING,
        unique     = False
    )
    rating  = models.FloatField()

    def __str__(self):
        return f'User: {self.user} | Item: {self.item} |  Rating: {self.rating}'
