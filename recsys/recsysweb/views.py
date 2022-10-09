from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, Interaction
from .forms import ItemForm, InteractionForm
from django.core.paginator import Paginator



# Create your views here.

def home(request):
    return render(request, 'single/home.html')

def recommendations(request):
    return render(request, 'single/recommendations.html')

def likes(request):
    return render(request, 'single/likes.html')

def create_item(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('items')
    else:
        return render(request, 'items/create.html', {'form': form})

def edit_item(request, id):
    item = Item.objects.get(id=id)
    form = ItemForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('items')
    else:
        return render(request, 'items/edit.html', {'form': form, 'id': id})

def list_items(request):
    items       = Item.objects.all()
    paginator   = Paginator(items, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'items/list.html', {'page': page_obj})

def remove_item(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('items')
