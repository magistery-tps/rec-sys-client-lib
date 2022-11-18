from django.db import models

# Create your models here.


class Item(models.Model):
    id          = models.AutoField(primary_key=True)
    name        = models.TextField(max_length = 500,  verbose_name = 'Name')
    description = models.TextField(max_length = 1000, verbose_name = 'Description')
    image       = models.TextField(max_length = 500,  verbose_name = 'Image URL')
    popularity  = models.FloatField(default   = 0,    verbose_name = 'Popularity')

    class Meta:
        indexes = [
            models.Index(fields=['popularity'])
        ]

    def __str__(self):
        return f'{self.name}'

class Interaction(models.Model):
#    user = models.ForeignKey(
#        'auth.User',
#        db_column  = 'user_id',
#        on_delete  = models.DO_NOTHING,
#        unique     = False
#   )
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

class DistancesMatrix(models.Model):
    id          = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=200, verbose_name='Name')
    description = models.TextField(max_length=1000, verbose_name='Description')

class DistancesMatrixCell(models.Model):
    row    = models.IntegerField(db_column='row')
    column = models.IntegerField(db_column='column')
    matrix = models.ForeignKey(
        DistancesMatrix,
        db_column  = 'distances_matrix_id',
        on_delete  = models.DO_NOTHING,
        unique     = False
    )
    value = models.FloatField()
    
    def __str__(self):
        return f'row: {self.row} | Column: {self.columns} | Value: {self.value}'


class Recommendations:
    def __init__(self, name, items):
        self.name  = name
        self.id    = name.replace(' ', '-')
        self.items = list(items)

    def is_empty(self): return len(self.items) == 0
