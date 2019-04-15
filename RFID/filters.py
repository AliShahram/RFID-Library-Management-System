from .models import *
from .forms import *
import django_filters
from django_filters import *

class ObjectFilter(django_filters.FilterSet):
    class Meta:
        model = Object
        fields = ['name', 'location', 'availability']
        filter_overrides = {
             models.CharField: {
                 'filter_class': django_filters.CharFilter,
                 'extra': lambda f: {
                     'lookup_expr': 'icontains',
                 },
            }
        }



class RecordsFilter(django_filters.FilterSet):
    date = IsoDateTimeFilter()
    print(date)
    class Meta:
        model = Records
        fields = ['date', 'type', 'status',]
        fields = {
            'type': ['exact'],
            'status': ['exact'],
            'date': ['icontains', 'date__year', 'date__month', 'date__day'],
        }
