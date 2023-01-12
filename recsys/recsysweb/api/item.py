from rest_framework import serializers, viewsets
from ..models import Item
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from taggit.managers import TaggableManager
from rest_framework.decorators import action
from rest_framework.response import Response
from ..domain import DomainContext
import django_filters
import logging
from taggit.serializers import  (TagListSerializerField,
                                TaggitSerializer)


ctx = DomainContext()

# Serializers define the API representation.
class ItemSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model  = Item
        fields = ['id', 'name', 'description', 'popularity', 'rating', 'votes', 'tags']

# ViewSets define the view behavior.
class ItemViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAuthenticated]

    queryset         = Item.objects.all()
    serializer_class = ItemSerializer
    filterset_fields = ['id', 'name', 'description', 'popularity', 'rating', 'votes']

    def get_queryset(self,*args,**kwargs):
        return ctx.item_service.find_by_tags(tags = self.request.query_params.getlist("tag"))

