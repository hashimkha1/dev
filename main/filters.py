import django_filters 
from accounts.models import Credential

class CredentialFilter(django_filters.FilterSet):
    class Meta:
        model=Credential
        # fields= '__all__'
        fields ={
        # 'category':['icontains'],
        'name':['icontains'],
        'link_name':['icontains'],
        # 'entry_date':['icontains'],
        }
        # fields ={'name','link_name','entry_date'}
        labels={
                'name':'credential',
                'link_name':'username/email',
        }