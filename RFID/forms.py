
#Django imports
from django import forms
from django.forms import ModelForm, TextInput, Form
from django.core.exceptions import ValidationError
import datetime

#Local Imports
from .models import *
from .choices import *

class AddUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'email', 'phone')
        labels = {
            "user_id": "",
            "first_name": "",
            "last_name": "",
            "email": "",
            "phone": "",
        }

        widgets = {'user_id' : TextInput(attrs={'class' : 'form-field', 'placeholder' : ' User ID'}),
                    'first_name' : TextInput(attrs={'class' : 'form-field', 'placeholder' : ' First Name'}),
                    'last_name' : TextInput(attrs={'class' : 'form-field', 'placeholder' : ' Last Name'}),
                    'email' : TextInput(attrs={'class' : 'form-field', 'placeholder' : ' Email Address'}),
                    'phone' : TextInput(attrs={'class' : 'form-field', 'placeholder' : ' Phone Number'}),
                    }


class GetUser(forms.Form):
    user_id = forms.CharField(max_length=32, label='', required=False,
    widget=forms.TextInput(attrs={'class' : 'form-field', 'placeholder' : ' User ID - Optional'})
    )

    email = forms.EmailField(label='', required=True,
    widget = forms.TextInput(attrs={'class' : 'form-field', 'placeholder' : ' Email'})
    )


class AddObject(forms.ModelForm):
    class Meta:
        model = Object
        fields = ('object_id', 'name', 'availability', 'max_time', 'location')
        labels = {
            "object_id": "",
            "name": "",
            "availability": "",
            "max_time": "",
            "location": "",
        }

        widgets = {'object_id' : TextInput(attrs={'class' : 'form-field', 'placeholder' : ' Object ID'}),
                    'name' : TextInput(attrs={'class' : 'form-field', 'placeholder' : ' Name'}),
                    'max_time' : TextInput(attrs={'class' : 'form-field', 'placeholder' : ' Maximum Checkout in days'}),
                    }


class GetObject(forms.Form):
    object_id = forms.CharField(max_length=32, label='', required=False,
    widget=forms.TextInput(attrs={'class': 'form-field', 'placeholder': ' Object ID'})
    )

    name = forms.CharField(max_length=60, label='', required=True,
    widget=forms.TextInput(attrs={'class': 'form-field', 'placeholder': ' Name'})
    )



class GetGroupObject(forms.ModelForm):
    class Meta:
        model = Object
        fields = ('name', 'availability', 'max_time')
        labels = {
            "name": "",
            "availability": "",
            "max_time": "",
        }

        widgets = {'name' : TextInput(attrs={'class' : 'form-field', 'placeholder' : ' Name'}),
                    'max_time' : TextInput(attrs={'class' : 'form-field', 'placeholder' : ' Maximum Checkout in days'}),
                    }


class SearchBar(forms.Form):

    table = forms.CharField(max_length=50, label='', required=True)

    name = forms.CharField(max_length=50, label='', required=False,
    widget=forms.TextInput(attrs={'class':'form-field', 'placeholder': 'Search...'}))

    location = forms.ChoiceField(choices = OBJ_LOCATION_CHOICES, label="", initial='', required=False,
    widget=forms.Select(attrs={'class':'form-field'}))

    availability = forms.ChoiceField(choices = OBJ_AVAILABILITY_CHOICES, label="", initial='', required=False,
    widget=forms.Select(attrs={'class':'form-field'}))

    record_date = forms.DateField(initial='', label="Date", required=False)

    record_status = forms.ChoiceField(choices = RECORD_STATUS_CHOICES, label="", initial='', required=False,
    widget=forms.Select(attrs={'class':'form-field'}))
