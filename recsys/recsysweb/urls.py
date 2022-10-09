from django.urls import path
from .import views

urlpatterns = [ 
    path('', views.home, name='home'),
    path('recommendations', views.recommendations, name='recommendations'),
    path('likes', views.likes, name='likes'),

    path('items', views.list_items,          name='items'),
    path('items/create', views.create_item, name='items.create'),
    path('items/edit', views.edit_item,     name='items.edit'),
    path('items/remove', views.remove_item, name='items.remove')
]
