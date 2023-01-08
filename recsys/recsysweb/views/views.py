from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Domain
from ..service      import RecommenderService, InteractionService


interaction_service = InteractionService()
recommender_service = RecommenderService()



@login_required
def home(request):
    user_n_interactions = interaction_service.count_by_user(request.user)
    response = {
        'user_n_interactions': user_n_interactions
    }
    return render(request, 'single/home.html', response)
