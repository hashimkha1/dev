import django_filters 
from accounts.models import Credential
from management.models import Requirement,TaskHistory,Task
from finance.models import Food
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
class TaskHistoryFilter(django_filters.FilterSet):
    class Meta:
        model=TaskHistory
        # fields= '__all__'
        fields ={
                'group':['icontains'],
                'activity_name':['icontains']
        }
        labels={
                'employee'
                'activity_name':'Task',
                'group':'Group',
        }
class TaskFilter(django_filters.FilterSet):
    class Meta:
        model=Task
        # fields= '__all__'
        fields ={
                'group':['icontains'],
                'activity_name':['icontains']
        }
        labels={
                'activity_name':'Task',
                'group':'Group',
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
    
class FoodFilter(django_filters.FilterSet):
    class Meta:
        model=Food
        # fields='__all__'
        fields ={'supplier','item'}
    