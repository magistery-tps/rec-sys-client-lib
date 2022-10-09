from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, Interaction
from .forms import ItemForm, InteractionForm
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def sign_in(request):
    if request.method != "POST":
        return render(request, 'authentication/sign_in.html')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        messages.success(request, 'There was an sign in error. Try again!')
        return redirect(request, 'authentication/sign_in.html')

@login_required
def sign_out(request):
    logout(request)
    return redirect('sign-in')

@login_required
def home(request):
    return render(request, 'single/home.html')

@login_required
def recommendations(request):
    return render(request, 'single/recommendations.html')

@login_required
def likes(request):
    return render(request, 'single/likes.html')

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
