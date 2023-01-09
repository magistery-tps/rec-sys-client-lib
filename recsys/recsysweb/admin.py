from django.contrib import admin
from .models import (
    Item,
    Interaction,
    Recommender,
    SimilarityMatrixCell,
    SimilarityMatrix,
    RecommenderEnsemble,
    RecommenderEnsembleConfig,
    RecommenderEnsempleEvaluation,
    RecommenderEnsempleEvaluationMetric
)

# Register your models here.


@admin.register(RecommenderEnsempleEvaluation)
class RecommenderEnsempleEvaluationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'ensemble',
        'enable'
    ]


@admin.register(RecommenderEnsempleEvaluationMetric)
class RecommenderEnsempleEvaluationMetricAdmin(admin.ModelAdmin):
    list_display = [
        'evaluation',
        'user',
        'value'
    ]


@admin.register(RecommenderEnsemble)
class RecommenderEnsembleAdmin(admin.ModelAdmin):
    list_display = ['name', 'enable', 'position']


@admin.register(RecommenderEnsembleConfig)
class RecommenderEnsembleConfigAdmin(admin.ModelAdmin):
    list_display = [
        'recommender',
        'active_from_n_user_iterations',
        'active_to_n_user_iterations',
        'n_items_by_session'
    ]


@admin.register(SimilarityMatrix)
class SimilarityMatrixAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'version']


@admin.register(SimilarityMatrixCell)
class SimilarityMatrixCellAdmin(admin.ModelAdmin):
    list_display = ['row', 'column', 'value', 'version']


@admin.register(Recommender)
class RecommenderAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'type',
        'enable',
        'position',
        'user_similarity_matrix',
        'item_similarity_matrix'
    ]


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'rating']


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