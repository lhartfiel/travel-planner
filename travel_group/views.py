from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, FormView
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token

from accommodations.models import Accommodations
from travel_users.models import CustomUser
from .models import TravelGroup, SightseeingIdeas, RestaurantIdeas, TravelMessages, ChecklistItems
from .forms import GroupCreateForm, SightseeingFormSet, RestaurantFormSet, MessageFormSet, SightseeingEditForm, \
    SightseeingCreateForm, RestaurantEditForm, RestaurantCreateForm, MessageCreateForm, ChecklistCreateForm, \
    ChecklistEditForm
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
import json

from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.core.mail import send_mail
from django.conf import settings



class TravelGroupListView(ListView):
    template_name = 'travel_group/group-list.html'
    queryset = TravelGroup.objects.all()
    context_object_name = 'travel_groups'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        context['trips'] = TravelGroup.objects.filter(travelers__username=username)
        return context


class TravelerAccommodationListView(ListView):
    model = TravelGroup
    template_name = 'accommodations/accommodation-travel-list.html'

    def get_context_data(self, **kwargs):
        username = self.kwargs['username']
        context = super().get_context_data(**kwargs)
        context['profile_user'] = username
        context['accommodations'] = Accommodations.objects.filter(trip__id=self.kwargs['pk'], user__username=username)
        return context


class TravelGroupSingleView(DetailView):
    model = TravelGroup
    template_name = 'travel_group/group-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = TravelMessages.objects.filter(travel_group=context.get('travelgroup'))
        context['message_form'] = MessageCreateForm(initial={'message_creator': self.request.user, 'travel_group': context.get('travelgroup')})
        return context


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
        data = request.POST.copy()
        data['messages-0-message_creator'] = self.request.user.id
        sightseeing_form = SightseeingFormSet(self.request.POST)
        restaurant_form = RestaurantFormSet(self.request.POST)
        message_form = MessageFormSet(data)
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
    form_class = MessageCreateForm
    template_name = 'travel_group/message-add.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.message_creator = self.request.user
        return form

    def form_valid(self, form):
        message_body = form.cleaned_data.get('message')
        message_group = form.cleaned_data.get('travel_group').trip_name
        message_group_id = form.cleaned_data.get('travel_group').id
        travelers = CustomUser.objects.filter(trav_groups=message_group_id)
        traveler_emails = []
        for traveler in travelers:
            traveler_emails.append(traveler.email)
        subject = 'A new message has been posted in ' + message_group
        message = message_body
        email_from = settings.EMAIL_HOST_USER
        recipient_list = traveler_emails
        send_mail(subject, message, email_from, recipient_list)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('travel_group_single', kwargs={'pk': self.kwargs.get('id')})


class MessageEditView(UpdateView):
    model = TravelMessages
    template_name = 'travel_group/message-edit.html'


class TravelGroupChecklistView(CreateView):
    model = ChecklistItems
    form_class = ChecklistCreateForm
    template_name = 'travel_group/checklist-add.html'

    def form_valid(self, form):
        # TODO Verify that current user is submitting the form
        return super().form_valid(form)

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        initial = {'travel_group': self.kwargs.get('id'), 'checklist_creator': self.request.user}
        return initial

    def get_success_url(self):
        return reverse('travel_checklist_list', kwargs={'id': self.kwargs.get('id'), 'username': self.request.user})


class TravelGroupChecklistEditView(UpdateView):
    model = ChecklistItems
    template_name = 'travel_group/checklist-edit.html'
    form_class = ChecklistEditForm

    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST' and request.is_ajax():
            data = json.loads(request.body.decode('utf-8'))
            request.POST = request.POST.copy()
            request.POST = data
            form = self.form_class(request.POST)
            form.instance.checklist_creator_id = data['checklist_creator']
            form.instance.travel_group_id = data['travel_group']
            form.instance.checklist_item = data['checklist_item']
            form.instance.checklist_status = True
            form.instance.id = data['item_id']
            form.save()
            if form.is_valid():
                self.object = self.get_object()
                return super(TravelGroupChecklistEditView, self).post(request, *args, **kwargs)
        else:
            self.object = self.get_object()  # assign the object to the view
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)

    def get_initial(self):
        initial = self.initial.copy()
        obj = self.get_object()
        initial['checklist_item'] = self.object.checklist_item
        return initial

    def get_success_url(self):
        print('wrong')
        return reverse('travel_checklist_list', kwargs={'id': self.object.travel_group.id, 'username': self.request.user.username})


class TravelGroupChecklistList(ListView):
    model = ChecklistItems
    # queryset = ChecklistItems.objects.all()
    template_name = 'travel_group/checklist-list.html'

    def get_context_data(self, **kwargs):
        self
        context = super().get_context_data(**kwargs)
        context['items'] = ChecklistItems.objects.filter(travel_group__id=self.kwargs['id'])
        context['travelgroup'] = self.kwargs.get('id')
        context['checklist_create_form'] = ChecklistCreateForm(initial={'checklist_creator': self.request.user, 'travel_group': self.kwargs.get('id')})
        context['checklist_form'] = ChecklistEditForm(initial={'checklist_creator': self.request.user, 'travel_group': self.kwargs.get('id')})
        return context


class TravelGroupChecklistDelete(DeleteView):
    model = ChecklistItems
    template_name = 'travel_group/checklist-delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(ChecklistItems, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse('travel_checklist_list', kwargs={'id': self.object.travel_group.id, 'username': self.request.user.username})


# Serializers define the API representation.
class ChecklistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChecklistItems
        fields = ['checklist_item', 'item_status']


# ViewSets define the view behavior.
class ChecklistViewSet(viewsets.ModelViewSet):
    queryset = ChecklistItems.objects.all()
    serializer_class = ChecklistSerializer