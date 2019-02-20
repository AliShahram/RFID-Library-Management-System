from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from RFID.forms import *


#--- home page ----


class HomePageView(LoginRequiredMixin, View):
    """ if not authinticated direct them
    to the login page """

    login_url = '/RFID/login/'
    redirect_field_name = ''
    template_name = 'RFID/home.html'

    def post(self, request):
        form = PersonForm(request.POST)
        form.save()
        new_form = PersonForm()
        context = {'form':new_form}

        return render(request, self.template_name, context)

    def get(self, request):
        form = PersonForm()
        context = {'form':form}

        return render(request, self.template_name, context)


class UserPageView(LoginRequiredMixin, View):
    login_url = '/RFID/login/'
    redirect_field_name = ''
    template_name = 'RFID/user.html'

    def post(self, request):
        form = AddUser(request.POST)
        message = "The user was not added. Please try again!"

        # Validate if the information passed in post is valid
        if form.is_valid():
            form.save()
            message = "The user was successfuly added!"

        print(form.errors)    
        new_form = AddUser()
        context = {'form':new_form, 'message':message}

        return render(request, self.template_name, context)

    def get(self, request):
        form = AddUser()
        context = {'form':form}
        return render(request, self.template_name, context)


class ObjectPageView(LoginRequiredMixin, View):
    login_url = '/RFID/login/'
    redirect_field_name = ''
    template_name = 'RFID/object.html'

    def get(self, request):
        return render(request, self.template_name)
