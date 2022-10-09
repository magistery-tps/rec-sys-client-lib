from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'single/home.html')

def recommendations(request):
    return render(request, 'single/recommendations.html')

def likes(request):
    return render(request, 'single/likes.html')


def create_item(request):
    return render(request, 'items/create.html')

def edit_item(request):
    return render(request, 'items/edit.html')

def list_items(request):
    return render(request, 'items/list.html')

def remove_item(request):
    return list_items(request)
