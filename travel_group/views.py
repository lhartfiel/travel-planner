from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView,UpdateView, CreateView
from .models import TravelGroup, SightseeingIdeas, RestaurantIdeas, TravelMessages
from .forms import GroupCreateForm, SightseeingFormSet, RestaurantFormSet, MessageFormSet, SightseeingEditForm
from django.http import HttpResponseRedirect


class TravelGroupListView(ListView):
    template_name = 'travel_group/group-list.html'
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
    template_name = 'travel_group/group-detail.html'

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

# class TravelGroupCreateView(FormView):
#     model = TravelGroup
#     template_name = 'travel_group/group-create.html'
#     queryset = model.objects.none()

# class TravelGroupEditView(UpdateView):
#     model = TravelGroup
#     fields = ['travelers', 'trip_name']
#     template_name = 'travel_group/group-edit.html'


class TravelGroupCreateView(CreateView):
    """
    Custom Form for the Travel Group
    Based on http://kevindias.com/writing/django-class-based-views-multiple-inline-formsets/
    """
    model = TravelGroup
    template_name = 'travel_group/group-create.html'
    form_class = GroupCreateForm
    success_url = '/'

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


class SightseeingEditView(UpdateView):
    model = TravelGroup
    pk_url_kwarg = 'id'
    form_class = SightseeingEditForm
    template_name = 'travel_group/sightseeing-edit.html'

    def get_initial(self):
        original = SightseeingIdeas.objects.filter(travel_group_id=self.object.id)
        for item in original:
            return {'sightseeing_idea': item}

    # def form_valid(self, form):
    #     self.object = form.save()
    #     ideas = SightseeingIdeas.objects.all()
    #     for idea in ideas:
    #         idea.save()
    #         return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('travel_group_single', kwargs={'username': self.request.user.username, 'id': self.object.id})


class RestaurantEditView(UpdateView):
    model = RestaurantIdeas
    template_name = 'travel_group/restaurant-edit.html'


class MessageEditView(UpdateView):
    model = TravelMessages
    template_name = 'travel_group/message-edit.html'

