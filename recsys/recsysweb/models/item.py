from django.db import models


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
        return f'Name: {self.name} | Popularity: {self.popularity} | Image: {self.image} | Desc: {self.description}'

