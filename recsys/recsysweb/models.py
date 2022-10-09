from django.db import models

# Create your models here.


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='Name')
    description = models.TextField(max_length=1000, verbose_name='Description')
    image = models.CharField(max_length=255, verbose_name='Image URL')

    def __str__(self):
        return f'{self.name}'

class Interaction(models.Model):
    user = models.ForeignKey(
        'auth.User', 
        db_column  = 'user_id',  
        on_delete  = models.DO_NOTHING,
        unique     = False
    )
    item = models.ForeignKey(
        Item,
        db_column  = 'item_id',
        on_delete  = models.DO_NOTHING,
        unique     = False
    )
    rating  = models.FloatField()
    def __str__(self):
        return f'User: {self.user} | Item: {self.item} |  Rating: {self.rating}'


class Recommendations:
    def __init__(self, name, items):
        self.name  = name
        self.id    = name.replace(' ', '-')
        self.items = list(items)