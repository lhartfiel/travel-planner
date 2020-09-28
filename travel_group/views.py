import requests

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accommodations.models import Accommodations
from travel_users.models import CustomUser
from .models import TravelGroup, SightseeingIdeas, RestaurantIdeas, TravelMessages, ChecklistItems
from .forms import GroupCreateForm, SightseeingFormSet, RestaurantFormSet, MessageFormSet, SightseeingEditForm, \
    SightseeingCreateForm, RestaurantEditForm, RestaurantCreateForm, MessageCreateForm, ChecklistCreateForm, \
    ChecklistEditForm, MessageEditForm
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse
import json

from rest_framework import routers, serializers, viewsets
from django.core.mail import send_mail
from django.conf import settings


# class UnsplashPhoto(object):
#
#     def __init__(self, **kwargs):
#         for field in ('url', 'photographer', ):
#             setattr(self, field, kwargs.get(field, None))
#
#     photos = {}
#
#
# class UnsplashPhotoSerializer(serializers.Serializer):
#     url = serializers.URLField()
#     photographer = serializers.CharField()
#
#     def create(self, validated_data):
#         return UnsplashPhoto(**validated_data)

class TravelGroupImage(APIView):
    queryset = TravelGroup.objects.values_list('primary_destination')

    def get(self, request):
        photo_list = TravelGroup.objects.values_list('primary_destination', flat=True).distinct()
        filtered_list = list(filter(None, photo_list))
        photo_dict = dict()
        for photo in filtered_list:
            unsplash_api = f'https://api.unsplash.com/search/photos?client_id=TK4hk3RxTdHHy5yLPsfGKkROapr5q3i2hAOKp37joHM&query={photo}&page=1'
            try:
                response = requests.get(unsplash_api)
                response = response.json()
                photo_url = response['results'][0]["urls"]["regular"]
                photographer_name = response['results'][0]["user"]["name"]
                photo_dict[f'{photo}'] = {'url': photo_url, 'photographer': photographer_name}
            except AttributeError:
                pass
        context = {'results': photo_dict}
        return Response(context)


class TravelGroupListView(ListView):
    template_name = 'travel_group/group-list.html'
    queryset = TravelGroup.objects.all()
    context_object_name = 'travel_groups'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        photos = requests.get('http://127.0.0.1:8001/api-unsplash/?format=json')
        trips = TravelGroup.objects.filter(travelers__username=username)
        context['trips'] = trips
        context['photos'] = photos.json()["results"]
        return context


    # def get(self, request, *args, **kwargs):
    #     self
    #     photo_list = TravelGroup.objects.values_list('primary_destination', flat=True).distinct()
    #     # photo_list_encode = photo_list.join.replace(', ', '&').replace("'", "")
    #     # print(photo_list_encode)
    #
    #     request = requests.get('https://api.unsplash.com/search/photos?client_id=TK4hk3RxTdHHy5yLPsfGKkROapr5q3i2hAOKp37joHM&page=1&query=Italy')
    #     context = request
    #     return render(request, "travel_group/photo.html", context=context)


class TravelerAccommodationListView(ListView):
    model = TravelGroup
    template_name = 'accommodations/accommodation-travel-list.html'

    def get_context_data(self, **kwargs):
        username = self.kwargs['username']
        context = super().get_context_data(**kwargs)
        context['profile_user'] = username
        context['accommodations'] = Accommodations.objects.filter(trip__id=self.kwargs['pk'], user__username=username).order_by('date_check_in')
        return context


class TravelGroupSingleView(DetailView):
    model = TravelGroup
    template_name = 'travel_group/group-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = TravelMessages.objects.filter(travel_group=context.get('travelgroup')).order_by('-date_created_at')
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
        data_destination = form.data['primary_destination']

        unsplash_api = f'https://api.unsplash.com/search/photos?client_id=TK4hk3RxTdHHy5yLPsfGKkROapr5q3i2hAOKp37joHM' \
                       f'&query={data_destination}&page=1'
        response = requests.get(unsplash_api)
        response = response.json()
        photo_url = response['results'][0]["urls"]["regular"]
        photo_attribution = response['results'][0]["user"]["name"]

        data['messages-0-message_creator'] = self.request.user.id
        data['photo'] = photo_url
        data['travelers'] = form.data['travelers']
        user_logged_in = self.request.user.username
        try:
            users = data['travelers'].split(", ")
            users.append(user_logged_in)
            user_obj = CustomUser.objects.filter(username__in=users)
            data['travelers'] = user_obj #this must be a list
        except ObjectDoesNotExist:
            pass
        request.POST = data
        form = GroupCreateForm(self.request.POST)
        form.photo = photo_url
        sightseeing_form = SightseeingFormSet(self.request.POST)
        restaurant_form = RestaurantFormSet(self.request.POST)
        message_form = MessageFormSet(data)
        if form.is_valid() and sightseeing_form.is_valid() and restaurant_form.is_valid() and \
                message_form.is_valid():
            return self.form_valid(form, sightseeing_form, restaurant_form, message_form)
        else:
            self.form_invalid(form, sightseeing_form, restaurant_form, message_form)
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


class TravelGroupEditView(UpdateView):
    model = TravelGroup
    fields = ['travelers', 'trip_name', 'primary_destination']
    template_name = 'travel_group/group-edit.html'

    def get_success_url(self):
        self.object
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
        message_creator = self.request.user.first_name + ' ' + self.request.user.last_name
        traveler_emails = []
        for traveler in travelers:
            traveler_emails.append(traveler.email)
        subject = 'A new message has been posted in ' + message_group
        message = message_creator + ' wrote: ' + message_body
        email_from = settings.EMAIL_HOST_USER
        recipient_list = traveler_emails
        send_mail(subject, message, email_from, recipient_list)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('travel_group_single', kwargs={'pk': self.kwargs.get('id')})


class MessageEditView(UpdateView):
    model = TravelMessages
    form_class = MessageEditForm
    template_name = 'travel_group/message-edit.html'

    def get_object(self, queryset=None):
        return get_object_or_404(TravelMessages, id=self.kwargs.get('id'))

    def get_success_url(self):
        return reverse('travel_group_single', kwargs={'pk': self.object.travel_group.pk})


class MessageDeleteView(DeleteView):
    model = TravelMessages
    template_name = 'travel_group/message-delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(TravelMessages, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse('travel_group_single', kwargs={'pk': self.object.travel_group.id })


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
        return reverse('travel_checklist_list', kwargs={'id': self.object.travel_group.id, 'username': self.request.user.username})


class TravelGroupChecklistList(ListView):
    model = ChecklistItems
    # queryset = ChecklistItems.objects.all()
    template_name = 'travel_group/checklist-list.html'

    def get_context_data(self, **kwargs):
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