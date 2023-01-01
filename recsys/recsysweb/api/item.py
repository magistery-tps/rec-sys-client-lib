from rest_framework import serializers, viewsets
from ..models import Item
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from taggit.managers import TaggableManager
from taggit.serializers import  (TagListSerializerField,
                                TaggitSerializer)

import django_filters

# Serializers define the API representation.
class ItemSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model  = Item
        fields = ['id', 'name', 'description', 'popularity', 'rating', 'votes']
        exclude = ['tags']
        filter_overrides = {
            TaggableManager: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

# ViewSets define the view behavior.
class ItemViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAuthenticated]

    queryset         = Item.objects.all()
    serializer_class = ItemSerializer
    filterset_fields = ['id', 'name', 'description', 'popularity', 'rating', 'votes']
