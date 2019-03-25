from django.urls import path
from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [
    path('', UserHomePage.as_view(), name='UserHomePage'),
    path('user-search', UserSearch.as_view(), name='UserSearch'),

]
