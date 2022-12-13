from rest_framework import serializers, viewsets
from ..models import Interaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Serializers define the API representation.
class InteractionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model        = Interaction
        fields       = ['user', 'item', 'rating']
        lookup_field = 'interaction'


# ViewSets define the view behavior.
class InteractionViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAuthenticated]

    queryset         = Interaction.objects.all()
    serializer_class = InteractionSerializer
    filterset_fields = ['user', 'item', 'rating']
