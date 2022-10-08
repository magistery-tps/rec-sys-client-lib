from django.urls import path
from .import views

urlpatterns = [ 
    path('', views.home),
    path('recommendations', views.recommendations),
    path('likes', views.likes)
]
