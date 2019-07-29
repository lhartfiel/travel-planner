from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView

from accommodations.models import Accommodations
from .models import TravelGroup, SightseeingIdeas, RestaurantIdeas, TravelMessages
from .forms import GroupCreateForm, SightseeingFormSet, RestaurantFormSet, MessageFormSet, SightseeingEditForm, \
    SightseeingCreateForm, RestaurantEditForm, RestaurantCreateForm
from django.http import HttpResponseRedirect


class TravelGroupListView(ListView):
    template_name = 'travel_group/group-list.html'
    queryset = TravelGroup.objects.all()
    context_object_name = 'travel_groups'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trips'] = TravelGroup.objects.filter(travelers__id=self.request.user.id)
        return context


class TravelerAccommodationListView(ListView):
    model = TravelGroup
    template_name = 'accommodations/accommodation-travel-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accommodations'] = Accommodations.objects.filter(trip__id=self.kwargs['pk'])
        return context


class TravelGroupSingleView(DetailView):
    model = TravelGroup
    template_name = 'travel_group/group-detail.html'


class TravelGroupCreateView(CreateView):
    """
    Custom Form for the Travel Group
    Based on http://kevindias.com/writing/django-class-based-views-multiple-inline-formsets/
    """
    model = TravelGroup
    template_name = 'travel_group/group-create.html'
    form_class = GroupCreateForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        sightseeing_form = SightseeingFormSet()
        restaurant_form = RestaurantFormSet()
        message_form = MessageFormSet()
        return self.render_to_response(self.get_context_data(form=form, sightseeing_form=sightseeing_form, restaurant_form=restaurant_form, message_form=message_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        sightseeing_form = SightseeingFormSet(self.request.POST)
        restaurant_form = RestaurantFormSet(self.request.POST)
        message_form = MessageFormSet(self.request.POST)
        if form.is_valid() and sightseeing_form.is_valid() and restaurant_form.is_valid() and message_form.is_valid():
            return self.form_valid(form, sightseeing_form, restaurant_form, message_form)
        else:
            return self.form_invalid(form, sightseeing_form, restaurant_form, message_form)

    def form_valid(self, form, sightseeing_form, restaurant_form, message_form):
        self.object = form.save()
        sightseeing_form.instance = self.object
        sightseeing_form.save()
        restaurant_form.instance = self.object
        restaurant_form.save()
        message_form.instance = self.object
        message_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, sightseeing_form, restaurant_form, message_form):
        return self.render_to_response(self.get_context_data(form=form, sightseeing_form=sightseeing_form, restaurant_form=restaurant_form, message_form=message_form))

    def get_success_url(self):
        return reverse('travel_group_single', kwargs={'pk': self.object.id})


class SightseeingAddView(CreateView):
    model = SightseeingIdeas
    template_name = 'travel_group/sightseeing-add.html'
    form_class = SightseeingCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['travel_group'] = self.kwargs.get('pk')
        return kwargs

    def get_success_url(self):
        return reverse('travel_group_single', kwargs={'pk': self.kwargs.get('pk')})


class SightseeingDeleteView(DeleteView):
    model = SightseeingIdeas
    template_name = 'travel_group/sightseeing-delete.html'

    def get_success_url(self):
        return reverse('travel_group_single', kwargs={'pk': self.object.travel_group.id})


class SightseeingEditView(UpdateView):
    model = SightseeingIdeas
    form_class = SightseeingEditForm
    template_name = 'travel_group/sightseeing-edit.html'

    def get_success_url(self):
        return reverse('travel_group_single', kwargs={'pk': self.object.travel_group.id})


class RestaurantAddView(CreateView):
    model = RestaurantIdeas
    template_name = 'travel_group/restaurant-add.html'
    form_class = RestaurantCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['travel_group'] = self.kwargs.get('id')
        return kwargs

    def get_success_url(self):
        return reverse('travel_group_single', kwargs={'pk': self.kwargs.get('id')})


class RestaurantEditView(UpdateView):
    model = RestaurantIdeas
    form_class = RestaurantEditForm
    template_name = 'travel_group/restaurant-edit.html'

    def get_object(self, queryset=None):
        return get_object_or_404(RestaurantIdeas, id=self.kwargs.get('id'))

    def get_success_url(self):
        return reverse('travel_group_single', kwargs={'pk': self.object.travel_group.pk})


class RestaurantDeleteView(DeleteView):
    model = RestaurantIdeas
    template_name = 'travel_group/restaurant-delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(RestaurantIdeas, id=self.kwargs.get('id'))

    def get_success_url(self):
        return reverse('travel_group_single', kwargs={'pk': self.object.travel_group.id})


class MessageAddView(CreateView):
    model = TravelMessages
    template_name = 'travel_group/restaurant-add.html'
    form_class = MessageFormSet

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['travel_group'] = self.kwargs.get('id')
        return kwargs

    def get_success_url(self):
        return reverse('travel_group_single', kwargs={'pk': self.kwargs.get('id')})


class MessageEditView(UpdateView):
    model = TravelMessages
    template_name = 'travel_group/message-edit.html'

