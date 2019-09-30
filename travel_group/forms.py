from typing import Type, Optional, Any, Callable, Iterable

from django.forms import ModelForm, BaseModelFormSet, BaseModelForm, HiddenInput
from django import forms
from django.forms.utils import ErrorList
from django.shortcuts import get_object_or_404

from travel_group.models import TravelGroup, SightseeingIdeas, RestaurantIdeas, TravelMessages, ChecklistItems
from django.forms.models import inlineformset_factory

from travel_users.models import CustomUser


class GroupCreateForm(ModelForm):

    class Meta:
        model = TravelGroup
        fields = ['travelers', 'trip_name']


class SightseeingCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        travel_group = get_object_or_404(TravelGroup, id=kwargs.pop('travel_group'))
        super().__init__(*args, **kwargs)
        self.fields['travel_group'].initial = travel_group

    class Meta:
        model = SightseeingIdeas
        fields = ['sightseeing_idea', 'travel_group']
        widgets = {
            'travel_group': HiddenInput()
        }


class SightseeingEditForm(ModelForm):

    class Meta:
        model = SightseeingIdeas
        fields = ['sightseeing_idea']


class RestaurantCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        travel_group = get_object_or_404(TravelGroup, id=kwargs.pop('travel_group'))
        super().__init__(*args, **kwargs)
        self.fields['travel_group'].initial = travel_group
        self.fields['travel_group'].widget = forms.HiddenInput()

    class Meta:
        model = RestaurantIdeas
        fields = ['restaurant_idea', 'travel_group']


class RestaurantEditForm(ModelForm):
    class Meta:
        model = RestaurantIdeas
        fields = ['restaurant_idea']


class MessageCreateForm(ModelForm):
    class Meta:
        model = TravelMessages
        fields = ['message', 'travel_group', 'message_creator']
        widgets = {
            'message_creator': HiddenInput(),
            'travel_group': HiddenInput()
        }


class MessageEditForm(ModelForm):
    class Meta:
        model = TravelMessages
        fields = ['message', 'travel_group']


class ChecklistCreateForm(ModelForm):

    class Meta:
        model = ChecklistItems
        fields = ['checklist_item', 'checklist_creator', 'travel_group', 'item_status']
        widgets = {
            'checklist_creator': HiddenInput(),
            'travel_group': HiddenInput(),
        }


class ChecklistEditForm(ModelForm):
    class Meta:
        model = ChecklistItems
        fields = ['checklist_item', 'item_status']


SightseeingFormSet = inlineformset_factory(TravelGroup, SightseeingIdeas, extra=1, fields=('sightseeing_idea', ))
RestaurantFormSet = inlineformset_factory(TravelGroup, RestaurantIdeas, extra=1, fields=('restaurant_idea', ))
MessageFormSet = inlineformset_factory(TravelGroup, TravelMessages, extra=1, fields=('message', 'message_creator'))
ChecklistFormSet = inlineformset_factory(TravelGroup, ChecklistItems, extra=0, fields=('checklist_item', 'item_status'))
