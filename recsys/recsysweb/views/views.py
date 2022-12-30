from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Domain
from ..service      import RecommenderService


recommender_service = RecommenderService()



@login_required
def home(request):
    user_n_interactions = recommender_service.n_interactions_by(request.user)
    response = {
        'user_n_interactions': user_n_interactions
    }
    return render(request, 'single/home.html', response)
