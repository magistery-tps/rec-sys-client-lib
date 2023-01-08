from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


# Domain
from ..domain import DomainContext

ctx = DomainContext()


@login_required
def remove_all(request):
    ctx.interaction_service.remove_by_user(request.user)
    return redirect('recommendations')
