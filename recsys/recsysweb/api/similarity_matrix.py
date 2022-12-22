from rest_framework import serializers, viewsets
from ..models import SimilarityMatrix, SimilarityMatrixCell
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ..logger import get_logger


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


    @action(detail=False, methods=['GET'], url_path='versions')
    def get_versions(self, request, pk=None):
        versions = SimilarityMatrixCell \
            .objects \
            .filter(matrix__id=pk) \
            .values('version')  \
            .distinct()
        return Response(data=versions, status=status.HTTP_200_OK)


    @action(detail=False, methods=['DELETE'], url_path='versions/(?P<version>[0-9]+)')
    def delete_version(self, request, pk=None, version=None):
        models = SimilarityMatrixCell.objects.filter(matrix__id=pk, version=version)
        if models:
            response_body = {
                'matrix' : pk,
                'version': version,
                'deleted': len(models)
            }
            models.delete()
            return Response(data=response_body, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
