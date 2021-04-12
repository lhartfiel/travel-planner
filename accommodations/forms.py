from django.forms import ModelForm
from django import forms
from . models import Accommodations
from travel_transportation.forms import DateInputWidget


class AccommodationEditForm(ModelForm):

    class Meta:
        model = Accommodations
        fields = '__all__'
        widgets = {'date_check_in': DateInputWidget(), 'date_check_out': DateInputWidget(), 'phone': forms.TextInput(
            attrs={'placeholder': '+12345678901'}), 'website': forms.TextInput(
            attrs={'placeholder': 'https://'})}


class AccommodationCreateForm(ModelForm):

    class Meta:
        model = Accommodations
        fields = '__all__'
        widgets = {'date_check_in': DateInputWidget(), 'date_check_out': DateInputWidget(), 'phone': forms.TextInput(
            attrs={'placeholder': '+12345678901'}), 'website': forms.TextInput(
            attrs={'placeholder': 'https://'})}