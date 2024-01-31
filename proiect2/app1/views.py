from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView

from app1.models import location


# Create your views here.
class LocationView(ListView):
    model = location
    template_name = 'app1/location_index.html'

class CreateLocationView(CreateView):
    model = location
    fields = ['city', 'country']
    template_name = 'app1/location_form.html'

    def get_success_url(self):
        return reverse('app1:lista_locatii')