from rest_framework import serializers, viewsets
from ..models import SimilarityMatrixCell
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import logging
from rest_framework import generics, status
from rest_framework.response import Response


import logging

logging.basicConfig()
logging.getLogger('SimilarityMatrixCellRestResource').setLevel(logging.INFO)


class SimilarityMatrixCellBulkCreateUpdateSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        cellModels = [SimilarityMatrixCell(**item) for item in validated_data]
        return SimilarityMatrixCell.objects.bulk_create(cellModels)


# Serializers define the API representation.
class SimilarityMatrixCellSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model                 = SimilarityMatrixCell
        fields                = ['id', 'row', 'column', 'value', 'matrix', 'version']
        lookup_field          = 'SimilarityMatrixCell'
        list_serializer_class = SimilarityMatrixCellBulkCreateUpdateSerializer


# ViewSets define the view behavior.
class SimilarityMatrixCellViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAuthenticated]

    queryset         = SimilarityMatrixCell.objects.all()
    serializer_class = SimilarityMatrixCellSerializer
    filterset_fields = ['row', 'column', 'value', 'matrix', 'version']


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print('ERROR: ', e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_serializer(self, *args, **kwargs):
        # When data is an object list it setupo make  to True to peform a blukc database insertion.
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(SimilarityMatrixCellViewSet, self).get_serializer(*args, **kwargs)