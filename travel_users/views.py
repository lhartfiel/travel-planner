from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from travel_users.models import CustomUser
from travel_users.forms import CustomUserEditForm, UserCreationForm, CustomUserCreationForm
from django.views.generic import TemplateView, FormView


class ProfileView(FormView):
    form_class = AuthenticationForm
    template_name = 'travel_users/profile.html'

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/travel_users/profile')
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)


class ProfileEditView(FormView):
    template_name = 'travel_users/edit.html'
    form_class = CustomUserEditForm
    initial = {'key': ' value'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')


class UserSignupView(TemplateView):
    template_name = 'travel_users/signup.html'
    form_class = UserCreationForm
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
