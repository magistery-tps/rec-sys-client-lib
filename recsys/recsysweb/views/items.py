from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import logging

# Domain
from ..models       import Item
from ..forms        import ItemForm, InteractionForm
from ..service      import RecommenderService
from ..recommender  import RecommenderContext


recommender_service = RecommenderService()


@login_required
def create_item(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('items')
    else:
        return render(request, 'items/create.html', {'form': form})


@login_required
def edit_item(request, id, origin):
    item = Item.objects.get(id=id)
    form = ItemForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()

        if origin != 'detail':
            return redirect(origin)
        else:
            return render(request, 'items/edit.html', {'form': form, 'id': id, 'origin': origin})
    else:
        return render(request, 'items/edit.html', {'form': form, 'id': id, 'origin': origin})


@login_required
def detail_item(request, id, recommender_id):
    item = Item.objects.get(id=id)

    recommender = recommender_service.find_by_id(recommender_id)

    recommenders = [recommender] if recommender else recommender_service.find_by_user(request.user)

    detail = recommender_service.find_item_detail(recommenders, item)

    return render(request, 'items/detail.html', {'detail': detail})


@login_required
def list_items(request):
    items       = Item.objects.all()
    paginator   = Paginator(items, settings.ITEMS_PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)

    response = {
        'page'             : page_obj,
        'NO_IMAGE_ITEM_URL': settings.NO_IMAGE_ITEM_URL
    }
    return render(request, 'items/list.html', response)


@login_required
def remove_item(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('items')
