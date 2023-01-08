# django
from django.shortcuts               import render
from django.contrib.auth.decorators import login_required
from django.conf                    import settings

# Domain
from ..domain                       import DomainContext


ctx = DomainContext()

@login_required
def recommendations(request):
    recommendations_list = ctx.recommender_service.find_recommendations(request.user)
    user_n_interactions = ctx.interaction_service.count_by_user(request.user)

    response = {
        'recommendations'     : recommendations_list,
        'user_n_interactions' : user_n_interactions
    }
    if not recommendations_list:
        response['messages'] = ['Not found Items!']

    response['NO_IMAGE_ITEM_URL'] = settings.NO_IMAGE_ITEM_URL
    return render(request, 'single/recommendations.html', response)
