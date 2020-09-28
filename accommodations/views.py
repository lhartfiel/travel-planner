from django.urls import reverse
from collections import OrderedDict

from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import render

from accommodations.forms import AccommodationEditForm, AccommodationCreateForm
from accommodations.models import Accommodations


# Create your views here.
from travel_group.models import TravelGroup
from travel_users.models import CustomUser


class AccommodationListView(ListView):
    model = Accommodations
    template_name = 'accommodations/accommodation-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        places = self.object_list.all().order_by('date_check_in')
        username = self.kwargs['username']
        places_dict = {}
        for place in places:
            if place.trip not in places_dict:
                places_dict[place.trip] = [place]
            elif place.trip in places_dict:
                places_dict[place.trip].append(place)
        context['places'] = places_dict
        context['user_profile'] = CustomUser.objects.get(username=username)
        return context


class AccommodationListTravelGroupView(ListView):
    model = Accommodations
    template_name = 'accommodations/accommodation-list-travelgroup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        places = [self.object_list.get(trip_id=self.kwargs['pk'])]
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
    form_class = AccommodationCreateForm
    template_name = "accommodations/accommodation-create.html"

    def get_success_url(self):
        return reverse('accommodation_detail', kwargs={'username': self.object.user.username, 'pk': self.object.id})


class AccommodationEditView(UpdateView):
    model = Accommodations
    form_class = AccommodationEditForm
    template_name = 'accommodations/accommodation-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('accommodation_list', kwargs={'username': self.object.user.username})


class AccommodationDeleteView(DeleteView):
    model = Accommodations
    template_name = "accommodations/accommodation-delete.html"

    def get_success_url(self):
        return reverse('accommodation_list', kwargs={'username': self.object.user.username})

