from django.forms import ModelForm
from . models import Transportation
from django import forms


class TransportationEditForm(ModelForm):

    class Meta:
        model = Transportation
        fields = '__all__'
        # fields = ['__all__']
