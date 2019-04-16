#Django imports
from django.shortcuts import render, HttpResponse
from django.views import View


#Local imports
from .forms import *
from django.apps import apps
Object = apps.get_model('RFID', 'Object')
from .tools import *

# Create your views here.
class UserHomePage(View):
    template = 'student/home.html'


    def get(self, request):
        searchbar = SearchBar()
        checkform = Operation()
        context = {'searchForm':searchbar, 'checkform':checkform}
        return render(request, self.template, context)


class UserSearch(View):
    template = 'student/home.html'

    def get(self, request):
        searchbar = SearchBar(request.GET)
        name = searchbar['name'].value()

        querySet = Object.objects.filter(name__icontains=name)

        if querySet:
            message = None
        else:
            message = "The object does not exist in the system!"

        searchbar = SearchBar()
        checkform = Operation()
        context = {'searchForm':searchbar, 'message': message, 'qResult':querySet, 'checkform':checkform}
        return render(request, self.template, context)


class UserOperation(View):
    template = 'student/op_result.html'

    def post(self, request):
        form = Operation(request.POST)

        #Check if form is valid
        if form.is_valid():
            type = form.cleaned_data['type']
            if type == '1':
                result = perform_checkout(form)
            else:
                result = perform_checkin(form)

        context = {'qResult':result}
        return render(request, self.template, context)


class AboutPage(View):
    template = 'student/about.html'

    def get(self, request):
        return render(request, self.template)
