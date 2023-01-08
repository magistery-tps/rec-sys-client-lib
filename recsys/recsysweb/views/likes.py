# django
from django.shortcuts               import render
from django.contrib.auth.decorators import login_required
from django.conf                    import settings

# Domain
from ..forms                        import LikeForm
from ..domain                       import DomainContext


ctx = DomainContext()


@login_required
def likes(request):
    response = { 'score_levels': settings.SCORE_LEVELS }

    if request.method == "POST":
        form = LikeForm(request)
        ctx.item_service.score_item_by(form.item_id, request.user, form.rating)

    recommendations = ctx.recommender_service.find_recommendations_from_active_evaluation(request.user)

    user_n_interactions = ctx.interaction_service.count_by_user(request.user)

    if recommendations.empty:
        response['messages'] = ['Not found Items!']
    else:
        response['metadata']             = recommendations.metadata
        response['item']                = recommendations.items[0]
        response['user_n_interactions'] = user_n_interactions

    response['NO_IMAGE_ITEM_URL'] = settings.NO_IMAGE_ITEM_URL
    return render(request, 'single/likes.html', response)
