from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import random
from ..service import ItemRecService
from ..forms import LikeForm

item_rec_service = ItemRecService()


@login_required
def likes(request):
    response = { 'score_levels': settings.SCORE_LEVELS }

    if request.method == "POST":
        form = LikeForm(request)
        item_rec_service.rate_item_for(form.item_id, request.user, form.rating)
        print(form)

    recommendations = item_rec_service.find_items_non_scored_by(request.user)

    if recommendations.is_empty():
        response['messages'] = ['Not found Items!']
    else:
        response['item'] = recommendations.items[0]

    response['NO_IMAGE_ITEM_URL'] = settings.NO_IMAGE_ITEM_URL
    return render(request, 'single/likes.html', response)


@login_required
def recommendations(request):
    recs = item_rec_service.find_all(request.user)

    response = { 'recommendations': recs }
    if not recs:
        response['messages'] = ['Not found Items!']

    response['NO_IMAGE_ITEM_URL'] = settings.NO_IMAGE_ITEM_URL
    return render(request, 'single/recommendations.html', response)
