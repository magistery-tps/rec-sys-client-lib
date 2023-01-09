# django
from django.shortcuts               import render
from django.contrib.auth.decorators import login_required
from django.conf                    import settings
import logging


# Domain
from ..domain                       import DomainContext


ctx = DomainContext()


@login_required
def likes(request):
    if request.method == "POST":
        ctx.item_service.score_items_by(
            request.user,
            items_rating = get_item_rating(request)
        )

    recommendations = ctx.recommender_service \
        .find_recommendations_from_active_evaluation(request.user)

    response = build_response(recommendations, request.user)

    return render(request, 'single/likes.html', response)


def build_response(recommendations, user):
    response = {
        'score_levels' : settings.SCORE_LEVELS,
        'no_image_url' : settings.NO_IMAGE_ITEM_URL
    }

    if recommendations.empty:
        response['messages'] = ['Not found Items!']
    else:
        recommendations.items = recommendations.items[:5]
        response['recommendations']     = recommendations
        response['user_n_interactions'] = ctx.interaction_service.count_by_user(user)

    return response


def get_item_rating(request):
    return {int(key):int(value) for key, value in request.POST.items() if key != 'csrfmiddlewaretoken'}