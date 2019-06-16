from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView
from .forms import TransportationEditForm
from .models import Transportation
from django.urls import reverse


class TransportationListView(ListView):
    model = Transportation
    template_name = 'travel_transportation/transportation-list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['transportation'] = Transportation.objects.filter(user__id=self.request.user.id)
        return context


class TransportationDetailView(DetailView):
    model = Transportation
    template_name = 'travel_transportation/transportation-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class TransportationCreateView(CreateView):
    model = Transportation
    fields = '__all__'
    template_name = 'travel_transportation/transportation-create.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user.username})


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