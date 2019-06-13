from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Transportation
# Create your views here.


class TransportationEditView(UpdateView):
    model = Transportation
