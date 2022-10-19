from rest_framework import serializers, viewsets
from ..models import DistancesMatrixCell


# Serializers define the API representation.
class DistancesMatrixCellSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = DistancesMatrixCell
        fields = ['row', 'column', 'value', 'matrix']
        lookup_field = 'DistancesMatrixCell'


# ViewSets define the view behavior.
class DistancesMatrixCellViewSet(viewsets.ModelViewSet):
    queryset = DistancesMatrixCell.objects.all()
    serializer_class = DistancesMatrixCellSerializer
