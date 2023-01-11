from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


# Domain
from ..domain import DomainContext


ctx = DomainContext()


@login_required
@permission_required('recsysweb.reset_interactions')
def remove_all(request):
    ctx.interaction_service.remove_by_user(request.user)
    return redirect('recommendations')
