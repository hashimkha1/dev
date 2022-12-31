import django_filters 
from accounts.models import Credential
from management.models import Requirement

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

class RequirementFilter(django_filters.FilterSet):
    class Meta:
        model=Requirement
        # fields= '__all__'
        fields ={
        'category':['icontains'],
        'status':['icontains'],
        # 'company':['icontains'],
        'is_active':['icontains'],
        }
        # fields ={'name','link_name','entry_date'}
        # labels={
        #         'name':'credential',
        #         'link_name':'username/email',
        # }