from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView

from travel_group.models import TravelGroup
from travel_users.models import CustomUser
from .forms import TransportationEditForm, TransportationCreateForm
from .models import Transportation
from django.urls import reverse


class TransportationListView(ListView):
    model = Transportation
    template_name = 'travel_transportation/transportation-list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        username = self.kwargs['username']
        context['user_profile'] = CustomUser.objects.get(username=username)
        context['transportation'] = Transportation.objects.filter(user__username=username).order_by('travel_group')
        return context


class TransportationDetailView(DetailView):
    model = Transportation
    template_name = 'travel_transportation/transportation-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        username = self.kwargs['username']
        context['user_profile'] = CustomUser.objects.get(username=username)
        return context


class TransportationCreateView(CreateView):
    model = Transportation
    form_class = TransportationCreateForm
    template_name = 'travel_transportation/transportation-create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TransportationCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('transportation_list', kwargs={'username': self.request.user.username})


class TransportationEditView(UpdateView):
    model = Transportation
    form_class = TransportationEditForm
    template_name = 'travel_transportation/transportation-edit.html'

    def get_success_url(self):
        return reverse('transportation_detail', kwargs={'username': self.object.user.username, 'pk': self.object.pk})


class TransportationDeleteView(DeleteView):
    model = Transportation
    template_name = 'travel_transportation/transportation-delete.html'

    def get_success_url(self):
        return reverse('transportation_list', kwargs={'username': self.object.user.username})