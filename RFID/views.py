from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from RFID.forms import *
from RFID.models import *


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
        get_id_form = GetUserID()
        context = {'add_user_form':form, 'get_id_form':get_id_form, 'add_user_message':message, 'add_user_error': error}

        return render(request, self.template_name, context)

    def get(self, request):
        get_id_form = GetUserID()
        form = AddUser()
        context = {'add_user_form':form, 'get_id_form':get_id_form}
        return render(request, self.template_name, context)


class GetUserPageView(LoginRequiredMixin, View):
    login_url = '/RFID/login/'
    redirect_field_name = ''
    update_template = 'RFID/update_user.html'
    delete_template = 'RFID/delete_user.html'


    def get_user(self, user_form):
        if user_form['user_id'].value():
            id = user_form['user_id'].value()
            return get_object_or_404(User, user_id=id)
        else:
            user_email = user_form['email'].value()
            return get_object_or_404(User, email=user_email)

    def post(self, request):
        get_id_form = GetUserID(request.POST)
        obj = self.get_user(get_id_form)
        update_form = AddUser(instance=obj)
        context = {'update_form':update_form}
        return render(request, self.update_template, context)

"""
        if 'Update' in request.POST:
            return render(request, self.update_template, context)
        elif 'Delete' in request.POST:
            return render(request, self.delete_template, context)
"""

class UpdateUserPageView(LoginRequiredMixin, View):
    login_url = '/RFID/login/'
    redirect_field_name = ''
    template_name = 'RFID/user.html'

    def post(self, request):

        if 'Update' in request.POST:
            form = AddUser(request.POST)
            id = form['user_id'].value()
            obj = User.objects.get(user_id=id)
            obj.first_name = form['first_name'].value()
            obj.last_name = form['last_name'].value()
            obj.email = form['email'].value()
            obj.phone = form['phone'].value()


            obj.save()

            message = 'User information was successfuly updated'
            get_id_form = GetUserID()
            form = AddUser()
            context = {'add_user_form':form, 'get_id_form':get_id_form, 'add_user_message':message}
            return render(request, self.template_name, context)

        elif 'Delete' in request.POST:
            form = AddUser(request.POST)
            id = form['user_id'].value()
            user = get_object_or_404(User, user_id=id)
            user.delete()


            message = 'User information successfully deleted'
            get_id_form = GetUserID()
            form = AddUser()
            context = {'add_user_form':form, 'get_id_form':get_id_form, 'add_user_message':message}
            return render(request, self.template_name, context)


class ObjectPageView(LoginRequiredMixin, View):
    login_url = '/RFID/login/'
    redirect_field_name = ''
    template_name = 'RFID/object.html'

    def get(self, request):
        return render(request, self.template_name)
