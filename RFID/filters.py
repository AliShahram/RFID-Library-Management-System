from .models import *
from .forms import *
import django_filters

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
     class Meta:
         model = Records
         fields = ['date', 'type', 'status',]
