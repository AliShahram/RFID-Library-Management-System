from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('user', UserPageView.as_view(), name='user'),
    path('object', ObjectPageView.as_view(), name='object'),
    path('search', HomePageView.as_view(), name='home'),
    path('add-user', UserPageView.as_view(), name='add-user'),

]
