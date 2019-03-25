from django.urls import path
from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
]
