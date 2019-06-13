from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from travel_users.models import CustomUser
from travel_users.forms import CustomUserEditForm, UserCreationForm, CustomUserCreationForm, CustomUserChangeForm
from django.views.generic import TemplateView, FormView, UpdateView, CreateView, View
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView


class ProfileView(FormView):
    form_class = AuthenticationForm
    template_name = 'travel_users/profile.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user.username})


class ProfileEditView(UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'travel_users/edit.html'

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, username=self.request.user.username)

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user.username})


class UserLoginView(LoginView):
    template_name = 'travel_users/login.html'

    # redirect to profile/{username} when user is logged in
    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse('profile', kwargs={'username': self.request.user.username})


class UserLogoutView(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class UserSignupView(CreateView):
    model = CustomUser
    template_name = 'travel_users/signup.html'
    form_class = CustomUserCreationForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/signup/success/')
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        return super().form_valid(form)


class UserSignupSuccessView(TemplateView):
    template_name = 'travel_users/signup_success.html'

