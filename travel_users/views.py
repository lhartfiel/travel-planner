from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate, login
from travel_users.models import CustomUser
from travel_users.forms import CustomUserEditForm, UserCreationForm

# Create your views here.


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return render(request, 'users/login.html')

    else:
        return 'Oops, invalid login credentials'


def edit_view(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return redirect('/')
    else:
        edit_user = CustomUser.objects.get(username=request.GET.username)
        form = CustomUserEditForm(edit_user)
        return render(request, 'users/edit.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return redirect('/')
            # return render(request, 'travel_users/signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'users/signup.html', {'form': form})
