from rest_framework import serializers, viewsets
from ..models import Item
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Serializers define the API representation.
class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = Item
        fields = ['id', 'name', 'description']


# ViewSets define the view behavior.
class ItemViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
