from django import forms
from django.forms import ModelForm, TextInput
from .models import *

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name','last_name']


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
