from typing import Type, Optional, Any, Callable, Iterable

from django.forms import ModelForm, BaseModelFormSet, BaseModelForm
from django import forms
from django.forms.utils import ErrorList
from django.shortcuts import get_object_or_404

from travel_group.models import TravelGroup, SightseeingIdeas, RestaurantIdeas, TravelMessages
from django.forms.models import inlineformset_factory


class GroupCreateForm(ModelForm):
    # sightseeing = forms.ModelMultipleChoiceField(queryset=SightseeingIdeas.objects.all())

    class Meta:
        model = TravelGroup
        fields = ['travelers', 'trip_name']


class SightseeingCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        travel_group = get_object_or_404(TravelGroup, id=kwargs.pop('travel_group'))
        super().__init__(*args, **kwargs)
        self.fields['travel_group'].initial = travel_group
        self.fields['travel_group'].widget = forms.HiddenInput()

    class Meta:
        model = SightseeingIdeas
        fields = ['sightseeing_idea', 'travel_group']


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
    def __init__(self, *args, **kwargs):
        travel_group = get_object_or_404(TravelGroup, id=kwargs.pop('travel_group'))
        super().__init__(*args, **kwargs)
        self.fields['travel_group'].initial = travel_group
        self.fields['travel_group'].widget = forms.HiddenInput()

    class Meta:
        model = TravelMessages
        fields = ['message', 'travel_group']


class MessageEditForm(ModelForm):
    class Meta:
        model = TravelMessages
        fields = ['message', 'travel_group']


SightseeingFormSet = inlineformset_factory(TravelGroup, SightseeingIdeas, fields=('sightseeing_idea', ))
RestaurantFormSet = inlineformset_factory(TravelGroup, RestaurantIdeas, fields=('restaurant_idea', ))
MessageFormSet = inlineformset_factory(TravelGroup, TravelMessages, fields=('message', ))