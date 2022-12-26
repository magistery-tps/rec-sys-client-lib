from django.contrib import admin
from .models import Item, Interaction, Recommender, SimilarityMatrixCell, SimilarityMatrix

# Register your models here.
admin.site.register(Item)
admin.site.register(Interaction)
admin.site.register(Recommender)
admin.site.register(SimilarityMatrix)
admin.site.register(SimilarityMatrixCell)
