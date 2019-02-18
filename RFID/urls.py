from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('home', HomePageView.as_view(), name='home'),
    path('user', UserPageView.as_view(), name='user'),
    path('object', ObjectPageView.as_view(), name='object'),
]
