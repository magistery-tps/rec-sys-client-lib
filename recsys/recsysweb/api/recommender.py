from rest_framework import serializers, viewsets
from ..models import Recommender
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Serializers define the API representation.
class RecommenderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model        = Recommender
        fields       = [
            'id',
            'name',
            'user_similarity_matrix',
            'item_similarity_matrix',
            'max_similar_users',
            'max_items_by_similar_user',
            'position',
            'enable'
        ]


        lookup_field = 'Recommender'


# ViewSets define the view behavior.
class RecommenderViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAuthenticated]

    queryset         = Recommender.objects.all()
    serializer_class = RecommenderSerializer
    filterset_fields = [
            'name',
            'user_similarity_matrix',
            'item_similarity_matrix',
            'max_similar_users',
            'max_items_by_similar_user',
            'position',
            'enable'
        ]
