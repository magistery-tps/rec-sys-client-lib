from rest_framework import serializers, viewsets
from ..models import Interaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response



# Serializers define the API representation.
class InteractionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model        = Interaction
        fields       = ['user', 'item', 'suitable_to_train', 'rating']
        lookup_field = 'interaction'


# ViewSets define the view behavior.
class InteractionViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes     = [IsAuthenticated]

    queryset         = Interaction.objects.all()
    serializer_class = InteractionSerializer
    filterset_fields = ['user', 'item', 'suitable_to_train', 'rating']


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_serializer(self, *args, **kwargs):
        # When data is an object list it setupo make  to True to peform a bulk database insertion.
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(InteractionViewSet, self).get_serializer(*args, **kwargs)