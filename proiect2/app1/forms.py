from django import forms
from django.forms import TextInput

from app1.models import location


class LocationForm(forms.ModelForm):

    class Meta:
        model = location
        fields = ['city', 'country']

        widgets = {
            'city': TextInput(attrs={'placeholder': 'city name', 'class': 'form-control'}),
            'country': TextInput(attrs={'placeholder': 'country name', 'class': 'form-control'}),
        }

    def __init__(self, pk, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.pk = pk

    def clean(self):
        city_value = self.cleaned_data.get('city')
        country_value = self.cleaned_data.get('country')
        if self.pk:
            if location.objects.filter(city__icontains=city_value, country__icontains=country_value).exclude(id=self.pk).exists():
                self._errors['city'] = self.error_class(['Orasul si tara deja exista!'])

        else:
            if location.objects.filter(city__icontains=city_value, country__icontains=country_value).exclude(id=self.pk).exists():
                self._errors['city'] = self.error_class(['Orasul si tara deja exista!'])

        return self.cleaned_data # minutul 42
