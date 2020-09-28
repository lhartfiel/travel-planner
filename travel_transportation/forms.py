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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'arrival_date' or visible.name == 'arrival_city' or visible.name == 'arrival_date':
                visible.field.widget.attrs['class'] = 'transport'

    class Meta:
        model = Transportation
        fields = ['name', 'travel_group', 'type', 'arrival_date', 'arrival_time', 'arrival_city', 'departure_date', 'departure_time',
                  'departure_city', 'carrier', 'flight_no', 'notes']
        labels = {
            "name": "Name (name this entry, such as Train from Rome to Florence)",
            "carrier": "Carrier (provide an optional carrier, such as United Airlines or Eurail)",
            "type": "Type of transportation (flight, train, ferry, etc)",
            "flight_no": "Flight no (optional)"
        }
        widgets = {'arrival_date': DateInputWidget(), 'departure_date': DateInputWidget(), 'arrival_time': TimeInputWidget(), 'departure_time': TimeInputWidget()}
