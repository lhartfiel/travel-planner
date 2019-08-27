from django.forms import ModelForm
from . models import Transportation
from django import forms


class DateInputWidget(forms.DateInput):
    """
    A widget for showing the datepicker
    """
    input_type = 'date'


class TimeInputWidget(forms.TimeInput):
    """
    A widget for showing the datepicker
    """
    input_type = 'time'


class TransportationEditForm(ModelForm):

    class Meta:
        model = Transportation
        exclude = ['user']
        widgets = {'arrival_date': DateInputWidget(), 'departure_date': DateInputWidget(), 'arrival_time': TimeInputWidget(), 'departure_time': TimeInputWidget()}


class TransportationCreateForm(forms.ModelForm):

    class Meta:
        model = Transportation
        exclude = ['user']
        widgets = {'arrival_date': DateInputWidget(), 'departure_date': DateInputWidget(), 'arrival_time': TimeInputWidget(), 'departure_time': TimeInputWidget()}
