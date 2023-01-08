from ..models import Interaction
from singleton_decorator import singleton

@singleton
class InteractionService:
    def count_by_user(self, user):
        return Interaction.objects.filter(user=user.id).count()


    def remove_by_user(self, user):
        Interaction.objects.filter(user=user.id).delete()