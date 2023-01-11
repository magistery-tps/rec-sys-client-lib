from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
import logging

# Domain
from ..models       import Item
from ..forms        import ItemForm, InteractionForm
from ..domain       import DomainContext
from ..recommender  import RecommenderContext, RecommenderCapability


ctx = DomainContext()


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
    item = ctx.item_service.find_by_id(id)
    form = ItemForm(request.POST or None, instance=item)

    logging.info(form)


    if form.is_valid():
        form.save()

        if origin != 'detail':
            return redirect(origin)
        else:
            user_n_interactions = ctx.interaction_service.count_by_user(request.user)
            response = {
                'form': form,
                'id': id,
                'origin': origin,
                'user_n_interactions': user_n_interactions
            }
            return render(request, 'items/edit.html', response)
    else:
        user_n_interactions = ctx.interaction_service.count_by_user(request.user)
        response = {
            'form': form,
            'id': id,
            'origin': origin,
            'user_n_interactions': user_n_interactions
        }
        return render(request, 'items/edit.html', response)


@login_required
def detail_item(request, id, recommender_id):
    item = ctx.item_service.find_by_id(id)

    recommenders = ctx.recommender_service \
        .find_by_user_recommender_id_and_capability(
            request.user,
            recommender_id,
            RecommenderCapability.SIMILARS
        )

    detail = ctx.recommender_service.find_item_detail(recommenders, item, request.user)
    user_n_interactions = ctx.interaction_service.count_by_user(request.user)

    response = {
        'detail': detail,
        'user_n_interactions': user_n_interactions
    }

    return render(request, 'items/detail.html', response)


@login_required
def list_items(request):
    tags = [t.replace('"', '') for t in request.GET.getlist('tag') if t]

    items_page = ctx.item_service.find_paginated(
        tags        = tags,
        page_number = request.GET.get('page'),
        page_size   = settings.ITEMS_PAGE_SIZE
    )

    response = {
        'page'                : items_page,
        'NO_IMAGE_ITEM_URL'   : settings.NO_IMAGE_ITEM_URL,
        'user_n_interactions' : ctx.interaction_service.count_by_user(request.user),
        'tags_uri'            : '&' + '&'.join([f'tag={t}' for t in tags]) if tags else '',
        'tags'                : ', '.join(tags)
    }

    return render(request, 'items/list.html', response)


@login_required
def remove_item(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('items')
