from rest_framework import serializers, viewsets
from ..models import DistancesMatrixCell
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Serializers define the API representation.
class DistancesMatrixCellSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = DistancesMatrixCell
        fields = ['id', 'row', 'column', 'value', 'matrix']
        lookup_field = 'DistancesMatrixCell'


# ViewSets define the view behavior.
class DistancesMatrixCellViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = DistancesMatrixCell.objects.all()
    serializer_class = DistancesMatrixCellSerializer
