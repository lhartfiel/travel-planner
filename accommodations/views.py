from audioop import reverse

from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, UpdateView, CreateView
from django.views.generic.list import ListView
from django.shortcuts import render

from accommodations.forms import AccommodationEditForm
from accommodations.models import Accommodations

# Create your views here.


class AccommodationListView(ListView):
    model = Accommodations
    template_name = 'accommodations/accommodation-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        places = self.object_list.all()
        places_dict = {}
        for place in places:
            if place.trip not in places_dict:
                places_dict[place.trip] = [place]
            elif place.trip in places_dict:
                places_dict[place.trip].append(place)
        context['places'] = places_dict
        return context


class AccommodationDetailView(DetailView):
    model = Accommodations
    template_name = "accommodations/accommodation-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AccommodationCreateView(CreateView):
    model = Accommodations
    fields = '__all__'
    template_name = "accommodations/accommodation-create.html"


class AccommodationEditView(UpdateView):
    model = Accommodations
    form_class = AccommodationEditForm
    template_name = 'accommodations/accommodation-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('accommodation_list', kwargs={'username': self.object.user.username, 'pk': self.object.pk})


class AccommodationDeleteView(TemplateView):
    template_name = "accommodations/accommodation-detail.html"
