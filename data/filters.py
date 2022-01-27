import django_filters 
from django_filters import DateFilter
from .forms import *
from .models import *


class InterviewFilter(django_filters.FilterSet):
    #start_date=DateFilter(field_name="upload_date",lookup_expr='gte')
    #end_date=DateFilter(field_name="upload_date",lookup_expr='lte')
    class Meta:
        model=InterviewUpload
        fields='__all__'
        exclude=['upload_date','doc','link']


'''
class InterviewFilter(django_filters.FilterSet):

     class Meta:
         model = InterviewUpload
         fields = ['first_name', 'upload_date']
         #fields='__all__'
         filter_overrides = {
             models.CharField: {
                 'filter_class': django_filters.CharFilter,
                 'extra': lambda f: {
                     'lookup_expr': 'icontains',
                 },
             },
             models.BooleanField: {
                 'filter_class': django_filters.BooleanFilter,
                 'extra': lambda f: {
                     'widget': forms.CheckboxInput,
                 },
             },
         }
''' 