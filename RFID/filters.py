from .models import *
import django_filters

class ObjectFilter(django_filters.FilterSet):
    class Meta:
        model = Object
        fields = ['name', 'location', 'availability', ]
