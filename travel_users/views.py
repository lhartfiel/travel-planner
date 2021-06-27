import json

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.base import View

from travel_group.forms import ChecklistCreateForm
from travel_group.models import ChecklistItems, TravelGroup
from travel_users.models import CustomUser
from travel_users.forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.generic import TemplateView, FormView, UpdateView, CreateView, DetailView, ListView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView


# class ProfileView(DetailView):
class ProfileView(TemplateView):
    model = CustomUser
    template_name = 'travel_users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(CustomUser, username=kwargs.get('username'))
        return context


class ProfileEditView(UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'travel_users/edit.html'

    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST' and request.is_ajax():
            data = json.loads(request.body.decode('utf-8'))
            request.POST = request.POST.copy()
            request.POST = data
            user_obj = self.get_object()
            travel_group_id = data.get('travel_group')
            if travel_group_id:
                travel_group_obj = TravelGroup.objects.get(id=travel_group_id)
                travel_group_obj.travel_group_invite.remove(user_obj)
            return HttpResponseRedirect(self.get_success_url())
        elif self.request.method == "POST":
            request.POST = request.POST.copy()
            user_obj = self.get_object()
            return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, username=self.request.user.username)

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user.username})


class ChecklistAllView(TemplateView):
    model = CustomUser
    template_name = 'travel_users/checklist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = kwargs.get('username')
        user = CustomUser.objects.get(username=username)
        context['checklists'] = TravelGroup.objects.filter(checklist_items__checklist_creator_id=user.id).distinct()
        return context



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
            travel_group = self.kwargs.get('travel_group_id')
            if travel_group:
                data = self.request.POST.copy()
                traveler_username = form.data['username']
                all_travelers = list(
                    TravelGroup.objects.get(pk=travel_group).travelers.all().values_list('username', flat=True))
                all_travelers.append(traveler_username)
                current_travel_group_obj = TravelGroup.objects.get(pk=travel_group)
                current_travel_group_obj.travelers.add(CustomUser.objects.get(username=traveler_username))
                current_travel_group_obj.save()
            return HttpResponseRedirect('/signup/success/')
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        return super(UserSignupView, self).form_valid(form)


class UserSignupSuccessView(TemplateView):
    template_name = 'travel_users/signup_success.html'

