from django import forms
from django.forms import ModelForm, TextInput
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('first_name','last_name')
        first_name = forms.CharField(label='First name')
        last_name = forms.CharField(label='Last name')
