from django.contrib import admin
from .models import Item, Interaction, Recommender, SimilarityMatrixCell, SimilarityMatrix

# Register your models here.
admin.site.register(Interaction)
admin.site.register(Recommender)
admin.site.register(SimilarityMatrix)
admin.site.register(SimilarityMatrixCell)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['tag_list']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    list_display = ['name', 'get_tags', 'id']


    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')


    def get_tags(self, obj):
        return u", ".join(o.name for o in obj.tags.all())