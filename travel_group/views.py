import requests

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django import forms
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.base import View, RedirectView
from django.views.generic.edit import FormMixin, FormView
from rest_framework.response import Response
from rest_framework.views import APIView

from accommodations.models import Accommodations
from travel_users.models import CustomUser
from .models import TravelGroup, SightseeingIdeas, RestaurantIdeas, TravelMessages, ChecklistItems, UnsplashPhotos
from .forms import GroupCreateForm, SightseeingFormSet, RestaurantFormSet, MessageFormSet, SightseeingEditForm, \
    SightseeingCreateForm, RestaurantEditForm, RestaurantCreateForm, MessageCreateForm, ChecklistCreateForm, \
    ChecklistEditForm, MessageEditForm, AddUserForm, RemoveUserForm
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse, request, HttpResponse
import json

from rest_framework import routers, serializers, viewsets
from django.core.mail import send_mail
from django.conf import settings


# invite = Invitation.create('email@example.com', inviter=request.travel_user)
# invite.send_invitation(request)

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


class InviteFormView(TemplateView):
    template_name = "travel_group/invite-form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['travel_user'] = kwargs.get('username')
        return context


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
        traveler = CustomUser.objects.get(username=username)
        photos = requests.get('http://127.0.0.1:8001/api-unsplash/?format=json')
        trips = TravelGroup.objects.filter(travelers__username=username).order_by('-transportation__departure_date')
        context['trips'] = trips
        context['photos'] = photos.json()["results"]
        context['traveler'] = traveler
        return context


class TravelGroupAddTraveler(FormView):
    form_class = AddUserForm
    template_name = 'travel_group/update-travelers.html'

    def get_context_data(self, **kwargs):
        context = super(TravelGroupAddTraveler, self).get_context_data(**kwargs)
        context['travel_group'] = self.kwargs.get('pk')
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        # perform a action here
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        data = self.request.POST.copy()
        traveler_email = form.data['traveler']
        current_travel_group = self.kwargs.get('pk')
        current_travel_group_obj = TravelGroup.objects.get(pk=current_travel_group)
        try:
            current_user = CustomUser.objects.get(email__exact=traveler_email)

            if current_user:
                all_travelers = list(TravelGroup.objects.get(pk=current_travel_group).travelers.all().values_list('username', flat=True))
                all_travelers.append(current_user.username)
                invited_traveler = CustomUser.objects.get(email=traveler_email)
                invited_traveler.save()
                return HttpResponseRedirect(self.get_success_url())
        except ObjectDoesNotExist:
            return HttpResponseRedirect(self.send_mail(form, traveler_email, self.request.user, current_travel_group))

    def get_success_url(self):
        return reverse('travel_group_single', kwargs={'pk': self.kwargs['pk']})

    def send_mail(self, form, email, sender, travel_group):
        # Send mail to admin with valid_data['order'] and valid_data['name']
        traveler_emails = []
        recipient_email = email
        message_creator = sender
        travel_group_name = TravelGroup.objects.get(pk=travel_group)
        html_message = render_to_string('mail_template.html', {'travel_group': travel_group, 'inviter':  message_creator})
        plain_message = strip_tags(html_message)
        subject = message_creator.first_name + ' has invited you to ' + travel_group_name.trip_name + ' on Travel Planner'
        email_from = settings.EMAIL_HOST_USER
        traveler_emails.append(recipient_email)
        self.request.session['recipient'] = recipient_email
        send_mail(subject, plain_message, email_from, traveler_emails, html_message=html_message)
        return reverse('travel_group_invite_sent', kwargs={'pk': travel_group})


class TravelGroupInviteSentView(TemplateView):
    template_name = 'travel_group/invite-sent.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TravelGroupInviteSentView, self).get_context_data(**kwargs)
        recipient = self.request.session.get('recipient')
        context['travel_group'] = TravelGroup.objects.get(id=kwargs.get('pk'))
        context['recipient'] = recipient
        return context

class TravelGroupRemoveUserView(FormView):
    form_class = RemoveUserForm
    template_name = 'travel_group/remove-travelers.html'

    def get_context_data(self, **kwargs):
        context = super(TravelGroupRemoveUserView, self).get_context_data(**kwargs)
        travel_group = self.kwargs.get('pk')
        context['travel_group'] = TravelGroup.objects.get(id=travel_group)
        context['traveler'] = self.kwargs.get('username')
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        # perform a action here
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        data = self.request.POST.copy()
        current_travel_group = self.kwargs.get('pk')
        current_travel_group_obj = TravelGroup.objects.get(pk=current_travel_group)
        user_to_remove = self.kwargs.get('username')
        all_travelers = list(
            TravelGroup.objects.get(pk=current_travel_group).travelers.all().values_list('username',
                                                                                         flat=True))
        all_travelers.remove(user_to_remove)
        user_obj = CustomUser.objects.filter(username__in=all_travelers)
        data['travelers'] = user_obj
        current_travel_group_obj.travelers.set(user_obj)  # this must be a list
        current_travel_group_obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('travel_group_index', kwargs={'username': self.kwargs['username']})


class TravelGroupInvitePendingView(TemplateView):
    template_name = 'travel_group/invite-pending.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TravelGroupInvitePendingView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['travel_group'] = TravelGroup.objects.get(id=kwargs.get('pk'))
        return context




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

        unsplash_api = unsplash_api = f'https://api.unsplash.com/search/photos?client_id=TK4hk3RxTdHHy5yLPsfGKkROapr5q3i2hAOKp37joHM&query={data_destination}&page=1'
        response = requests.get(unsplash_api)
        response = response.json()
        if len(response['results']) == 0:
            unsplash_general_photo = f'https://api.unsplash.com/search/photos?client_id' \
                                     f'=TK4hk3RxTdHHy5yLPsfGKkROapr5q3i2hAOKp37joHM&query="Travel"&page=1'
            response = requests.get(unsplash_general_photo)
            response = response.json()
        photo_url = response['results'][0]["urls"]["regular"]
        photo_attribution = response['results'][0]["user"]["name"]
        data['messages-0-message_creator'] = self.request.user.id
        user_logged_in = self.request.user.username

        try:
            users = []
            users.append(user_logged_in)
            user_obj = CustomUser.objects.filter(username__in=users)
            data['travelers'] = user_obj #this must be a list
        except ObjectDoesNotExist:
            pass
        request.POST = data
        form = GroupCreateForm(self.request.POST)

        sightseeing_form = SightseeingFormSet(self.request.POST)
        restaurant_form = RestaurantFormSet(self.request.POST)
        message_form = MessageFormSet(data)
        if form.is_valid() and sightseeing_form.is_valid() and restaurant_form.is_valid() and message_form.is_valid():
            return self.form_valid(form, user_logged_in, photo_url, photo_attribution, sightseeing_form, restaurant_form, message_form)
        else:
            errors = form.errors.as_data()
            self.form_invalid(form, sightseeing_form, restaurant_form, message_form)
            return self.form_invalid(form, sightseeing_form, restaurant_form, message_form)

    def form_valid(self, form, current_user, photo_url, photo_attribution, sightseeing_form, restaurant_form, message_form):
        self.object = form.save()
        new_photo = UnsplashPhotos(
            photo=photo_url,
            photo_attribution=photo_attribution,
            travel_group=form.instance
        )
        new_photo.save()
        form.group_owner = current_user
        form.save()
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

    def post(self, request, *args, **kwargs):
        if self.request.method == 'POST' and request.is_ajax():
            data = json.loads(request.body.decode('utf-8'))
            request.POST = request.POST.copy()
            request.POST = data
            travel_obj = self.get_object()
            all_travelers = list(travel_obj.travelers.all())
            traveler = data.get('traveler')
            traveler_obj = CustomUser.objects.get(username=traveler)
            all_travelers.append(traveler_obj)
            travel_obj.travelers.set(all_travelers)
            travel_obj.save()
            return super(TravelGroupEditView, self).post(request, *args, **kwargs)
        elif self.request.method == "POST":
            request.POST = request.POST.copy()
            return super().post(request, *args, **kwargs)

    def get_success_url(self):
        data_destination = self.object.primary_destination
        unsplash_api = f'https://api.unsplash.com/search/photos?client_id=TK4hk3RxTdHHy5yLPsfGKkROapr5q3i2hAOKp37joHM&query={data_destination}&page=1'
        response = requests.get(unsplash_api)
        response = response.json()
        photo_url = response['results'][0]["urls"]["regular"]
        photo_attribution = response['results'][0]["user"]["name"]
        new_photo = UnsplashPhotos(
            photo=photo_url,
            photo_attribution=photo_attribution,
            travel_group=self.object
        )
        new_photo.save()
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