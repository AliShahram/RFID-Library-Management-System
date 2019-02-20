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


    def get(self, request):

        return render(request, self.template_name)


class UserPageView(LoginRequiredMixin, View):
    login_url = '/RFID/login/'
    redirect_field_name = ''
    template_name = 'RFID/user.html'

    def post(self, request):
        add_user_form = AddUser(request.POST)
        message = "The user was not added. Please try again!"

        # Validate if the information passed in post is valid
        if add_user_form.is_valid():
            add_user_form.save()
            message = "The user was successfuly added!"

        error = add_user_form.errors
        form = AddUser()
        context = {'add_user_form':form, 'add_user_message':message, 'add_user_error': error}

        return render(request, self.template_name, context)

    def get(self, request):
        form = AddUser()
        context = {'add_user_form':form}
        return render(request, self.template_name, context)


class ObjectPageView(LoginRequiredMixin, View):
    login_url = '/RFID/login/'
    redirect_field_name = ''
    template_name = 'RFID/object.html'

    def get(self, request):
        return render(request, self.template_name)
