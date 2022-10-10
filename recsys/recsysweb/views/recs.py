from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..service import ItemRecService


item_rec_service = ItemRecService()


@login_required
def likes(request):
    if request.method == "POST":
        item_id, rating = request.POST['item_id'], request.POST['rating']
        item_rec_service.rate_item_for(item_id, request.user, rating)
        return redirect('likes')
    else:
        items = item_rec_service.find_unrated_by(request.user)

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
