from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..service import ItemRecService
from ..forms import LikeForm

item_rec_service = ItemRecService()


@login_required
def likes(request):
    if request.method == "POST":
        form = LikeForm(request)
        print(form)
        item_rec_service.rate_item_for(form.item_id, request.user, form.rating)
        return redirect('likes')
    else:
        items = item_rec_service.find_items_non_scored_by(request.user)

        response = {}
        if items:
            response['item'] = items[0]
        else:
            response['messages'] = ['Not found Items!']
        return render(request, 'single/likes.html', response)


@login_required
def recommendations(request):
    recs = item_rec_service.find_all(request.user)

    response = { 'recommendations': recs }
    if not recs:
        response['messages'] = ['Not found Items!']

    return render(request, 'single/recommendations.html', response)
