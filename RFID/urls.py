from django.urls import path
from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('user', UserPageView.as_view(), name='user'),
    path('object', ObjectPageView.as_view(), name='object'),
    path('search', HomePageView.as_view(), name='home'),
    path('get-user', GetUserPageView.as_view(), name='get-user'),
    path('update-user', UpdateUserPageView.as_view(), name='update-user'),
    path('get-object', GetObjectPageView.as_view(), name='get-object'),
    path('update-single-object', UpdateSingleObjectView.as_view(), name='update-single-object'),
    path('update-group-object', UpdateGroupObjectView.as_view(), name='update-group-object'),
]
