from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView, CreateView, View
from travel_group.models import TravelGroup, SightseeingIdeas, RestaurantIdeas, TravelMessages
from django.conf import settings
# Create your views here.


class TravelGroupListView(ListView):
    template_name = 'travel_group/index.html'
    queryset = TravelGroup.objects.all()
    context_object_name = 'travel_groups'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trips'] = TravelGroup.objects.all()
        return context

    def get_success_url(self):
        return reverse('travel_group', kwargs={'username': self.request.user.username})


class TravelGroupSingleView(DetailView):
    model = TravelGroup
    pk_url_kwarg = 'id'
    template_name = 'travel_group/travel_group_single-page.html'

    def get_context_data(self, **kwargs):
        current_trip = self.object.id
        sightseeing_ideas = SightseeingIdeas.objects.filter(travel_group_id=current_trip)
        restaurant_ideas = RestaurantIdeas.objects.filter(travel_group_id=current_trip)
        travel_messages = TravelMessages.objects.filter(travel_group_id=current_trip)
        context = super().get_context_data(**kwargs)
        context['sightseeing'] = sightseeing_ideas
        context['restaurants'] = restaurant_ideas
        context['messages'] = travel_messages
        return context

    # def get_object(self):
    #     self
    #     return get_object_or_404(TravelGroup, pk=self.request.session['id'])
#
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['trip_details'] = TravelGroup.objects.get()
    #     return context
    #
    # def get_success_url(self):
    #     return reverse('travel_group', kwargs={'username': self.request.user.username, 'slug': self.request.travel_group.pk})