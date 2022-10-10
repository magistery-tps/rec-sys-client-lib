from django.shortcuts import render, redirect
from .models import Item
from .forms import ItemForm, InteractionForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def create_item(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('items')
    else:
        return render(request, 'items/create.html', {'form': form})

@login_required
def edit_item(request, id):
    item = Item.objects.get(id=id)
    form = ItemForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('items')
    else:
        return render(request, 'items/edit.html', {'form': form, 'id': id})

@login_required
def list_items(request):
    items       = Item.objects.all()
    paginator   = Paginator(items, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'items/list.html', {'page': page_obj})

@login_required
def remove_item(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('items')
