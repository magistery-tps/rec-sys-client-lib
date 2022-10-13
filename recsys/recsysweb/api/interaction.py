from rest_framework import serializers, viewsets
from ..models import Interaction


# Serializers define the API representation.
class InteractionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = Interaction
        fields = ['user', 'item', 'rating']
        lookup_field = 'interaction'


# ViewSets define the view behavior.
class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
