from rest_framework import serializers, viewsets
from ..models import SimilarityMatrix
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Serializers define the API representation.
class SimilarityMatrixSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = SimilarityMatrix
        fields = ['id', 'name', 'type', 'description', 'version']
        lookup_field = 'SimilarityMatrix'


# ViewSets define the view behavior.
class SimilarityMatrixViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = SimilarityMatrix.objects.all()
    serializer_class = SimilarityMatrixSerializer
    filterset_fields = ['name', 'type', 'description', 'version']
