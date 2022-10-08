from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'pages/home.html')

def recommendations(request):
    return render(request, 'pages/recommendations.html')

def likes(request):
    return render(request, 'pages/likes.html')
