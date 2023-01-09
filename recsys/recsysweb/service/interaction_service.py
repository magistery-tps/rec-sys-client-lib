from ..models import Interaction
from singleton_decorator import singleton

@singleton
class InteractionService:
    def __init__(self, ctx): self.ctx = ctx


    def count_by_user(self, user):
        return Interaction.objects.filter(user=user.id).count()


    def remove_by_user(self, user):
        Interaction.objects.filter(user=user.id).delete()
        self.ctx.evaluation_service.remove_metrics_by_user(user)
        self.ctx.similarity_matrix_service.remove_cells_by_user(user)