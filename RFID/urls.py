from django.urls import path
from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('user', UserPageView.as_view(), name='user'),
    path('object', ObjectPageView.as_view(), name='object'),
    path('search', HomePageView.as_view(), name='home'),
    path('add-user', UserPageView.as_view(), name='add-user'),
    path('get-user', GetUserPageView.as_view(), name='get-user'),
    path('update-user', UpdateUserPageView.as_view(), name='update-user'),
]
