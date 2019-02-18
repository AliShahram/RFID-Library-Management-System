from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView



class HomePageView(TemplateView):
    template_name = 'home.html'

class UserPageView(TemplateView):
    template_name = 'user.html'

class ObjectPageView(TemplateView):
    template_name = 'object.html'
