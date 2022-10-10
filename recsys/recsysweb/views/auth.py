from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def sign_in(request):
    if request.method != "POST":
        return render(request, 'single/sign_in.html')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        messages.success(request, 'There was an sign in error. Try again!')
        return render(request, 'single/sign_in.html')

@login_required
def sign_out(request):
    logout(request)
    return redirect('sign-in')

