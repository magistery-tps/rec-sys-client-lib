from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


# Domain
from ..models import Interaction


@login_required
def remove_all(request):
    Interaction.objects.filter(user=request.user.id).delete()
    return redirect('recommendations')
