# django
from django.shortcuts               import render, redirect
from django.contrib                 import messages
from django.contrib.auth.decorators import login_required
from django.conf                    import settings

# Domain
from ..forms                        import LikeForm
from ..service                      import ItemService, RecommenderService
from ..recommender                  import RecommenderContext


item_service        = ItemService()
recommender_service = RecommenderService()


@login_required
def likes(request):
    response = { 'score_levels': settings.SCORE_LEVELS }

    if request.method == "POST":
        form = LikeForm(request)
        item_service.score_item_by(form.item_id, request.user, form.rating)

    recommendations = recommender_service.find_items_non_scored_by(request.user)

    if recommendations.empty:
        response['messages'] = ['Not found Items!']
    else:
        response['item'] = recommendations.items[0]

    response['NO_IMAGE_ITEM_URL'] = settings.NO_IMAGE_ITEM_URL
    return render(request, 'single/likes.html', response)


@login_required
def recommendations(request):
    recommendations_list = recommender_service.find_recommendations(request.user)

    response = { 'recommendations': recommendations_list }
    if not recommendations_list:
        response['messages'] = ['Not found Items!']

    response['NO_IMAGE_ITEM_URL'] = settings.NO_IMAGE_ITEM_URL
    return render(request, 'single/recommendations.html', response)
