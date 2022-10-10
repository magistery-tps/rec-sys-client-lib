from django.urls import path
from .import views

urlpatterns = [ 
    path('', views.home, name='home'),
    path('sign-in',  views.sign_in,  name='sign-in'),
    path('sign-out', views.sign_out, name='sign-out'),

    path('recommendations', views.recommendations, name='recommendations'),
    path('likes',           views.likes,           name='likes'),

    path('items',                 views.list_items,   name='items'),
    path('items/create',          views.create_item,  name='items.create'),
    path('items/edit/<int:id>',   views.edit_item,    name='items.edit'),
    path('items/remove/<int:id>', views.remove_item,  name='items.remove')
]
