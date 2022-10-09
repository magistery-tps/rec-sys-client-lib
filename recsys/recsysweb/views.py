from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, Interaction
from .forms import ItemForm, InteractionForm

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
    items = Item.objects.all()
    return render(request, 'items/list.html', {'items': items})

def remove_item(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('items')
