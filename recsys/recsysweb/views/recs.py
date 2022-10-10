from django.shortcuts import render, redirect
from .models import Item, Interaction, Recommendations
from .service import ItemRecService
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection

item_rec_service = ItemRecService()


@login_required
def likes(request):
    if request.method == "POST":
        item_id = request.POST['item_id']
        item    = Item.objects.get(id=item_id)
        rating  = request.POST['rating']

        interaction = Interaction.objects.create(
            user   = request.user,
            item   = item,
            rating = rating
        )
        interaction.save()
        print(interaction)
        return redirect('likes')
    else:
        item_query = Item.objects.raw(f'SELECT it.id FROM recsys.recsysweb_item AS it LEFT JOIN recsys.recsysweb_interaction AS i ON it.id = i.item_id AND i.user_id != {request.user.id} ORDER BY i.rating DESC LIMIT 1')
        print(item_query)
        if item_query:
            item = item_query[0]
            return render(request, 'single/likes.html', {'item': item})
        else:
            return render(request, 'single/likes.html', {'messages': ['Not found Items!']})

@login_required
def recommendations(request):
    recs = item_rec_service.find_all(user=request.user)

    response = { 'recommendations': recs }
    if not recs:
        response['messages'] = ['Not found Items!']

    return render(request, 'single/recommendations.html', response)
