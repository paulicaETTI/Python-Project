from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

from app1.forms import LocationForm
from app1.models import location


# Create your views here.
class LocationView(ListView):
    model = location
    template_name = 'app1/location_index.html'

class CreateLocationView(CreateView):
    model = location
    # fields = ['city', 'country']
    form_class = LocationForm
    template_name = 'app1/location_form.html'

    def get_success_url(self):
        return reverse('app1:lista_locatii')

    def get_form_kwargs(self):
        data = super(CreateLocationView, self).get_form_kwargs()
        data.update({'pk': None})
        return data


class UpdateLocationView(UpdateView):
    model = location
    # fields = ['city', 'country']
    form_class = LocationForm
    template_name = 'app1/location_form.html'

    def get_success_url(self):
        return reverse('app1:lista_locatii')

    def get_form_kwargs(self):
        data = super(UpdateLocationView, self).get_form_kwargs()
        data.update({'pk': self.kwargs['pk']})
        return data

def deactivate_location(request, pk):
    location.objects.filter(id=pk).update(active=0)
    return redirect('app1:lista_locatii')

def activate_location(request, pk):
    location.objects.filter(id=pk).update(active=1)
    return redirect('app1:lista_locatii')
