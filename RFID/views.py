from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from RFID.forms import PersonForm


class HomePageView(LoginRequiredMixin, View):
    login_url = '/login/'
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
    login_url = '/login/'
    redirect_field_name = ''
    template_name = 'RFID/user.html'

    def get(self, request):
        return render(request, self.template_name)


class ObjectPageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = ''
    template_name = 'RFID/object.html'

    def get(self, request):
        return render(request, self.template_name)
