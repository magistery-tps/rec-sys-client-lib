from ..models import Interaction
from singleton_decorator import singleton

@singleton
class InteractionService:
    def count_by_user(self, user):
        return Interaction.objects.filter(user=user.id).count()
