#Django imports
from django import forms
from django.forms import ModelForm, TextInput, Form

#Local Imports
from .choices import *


class SearchBar(forms.Form):
    name = forms.CharField(max_length=50, label='', required=False,
    widget=forms.TextInput(attrs={'class':'form-field', 'placeholder': 'Search...'}))
