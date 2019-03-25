#Django imports
from django.shortcuts import render, HttpResponse
from django.views import View


#Local imports
from .forms import *
from django.apps import apps
Object = apps.get_model('RFID', 'Object')



# Create your views here.
class UserHomePage(View):
    template = 'student/home.html'


    def get(self, request):
        searchbar = SearchBar()
        context = {'searchForm':searchbar}
        return render(request, self.template, context)


class UserSearch(View):
    template = 'student/home.html'

    def get(self, request):
        searchbar = SearchBar(request.GET)
        name = searchbar['name'].value()

        querySet = Object.objects.filter(name__iexact=name)

        if querySet:
            message = None
        else:
            message = "The object does not exist in the system!"

        searchbar = SearchBar()
        context = {'searchForm':searchbar, 'message': message, 'qResult':querySet}
        return render(request, self.template, context)
