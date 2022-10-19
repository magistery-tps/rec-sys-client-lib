from rest_framework import serializers, viewsets
from ..models import DistancesMatrix


# Serializers define the API representation.
class DistancesMatrixSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = DistancesMatrix
        fields = ['name', 'description']
        lookup_field = 'DistancesMatrix'


# ViewSets define the view behavior.
class DistancesMatrixViewSet(viewsets.ModelViewSet):
    queryset = DistancesMatrix.objects.all()
    serializer_class = DistancesMatrixSerializer
