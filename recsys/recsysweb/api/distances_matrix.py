from rest_framework import serializers, viewsets
from ..models import DistancesMatrix
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Serializers define the API representation.
class DistancesMatrixSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = DistancesMatrix
        fields = ['id', 'name', 'description']
        lookup_field = 'DistancesMatrix'


# ViewSets define the view behavior.
class DistancesMatrixViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = DistancesMatrix.objects.all()
    serializer_class = DistancesMatrixSerializer
