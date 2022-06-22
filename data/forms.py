from django import forms
from django.db.models import Q
# from codapp.accounts.models import CustomerUser
from accounts.models import CustomerUser
from .models import Interviews ,DSU #, DocUpload
from accounts.models import CustomerUser
from django.db.models import Q
class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interviews
        fields =['client','category','question_type','doc','link']
        labels={
               # 'first_name':'First Name',
                'client':'username', 
                'category':'Category',
                'question_type':'Question',
                'doc':'Assignment',
                'link':'Google Share Url',
                }

'''
class UploadForm(forms.ModelForm):
    class Meta:
        model = DocUpload
        fields = ['id','doc_type','doc_name','doc','link']
        labels={
                'doc_type':'Document Type',
                'doc_name':'Document Name',
                'doc':'Document',
        }
'''

class DSUForm(forms.ModelForm):
    class Meta:
        model = DSU
        #fields =['client','category','question_type','doc','link']
        fields=['cohort','trained_by','client_name','type','category','task','plan','challenge','uploaded']
        labels={
                'cohort':'Cohort',
                'type':'Client/Staff?',
                'trained_by':'Client Name',
                'client_name':'Trainer', 
                'category':'Category',
                'task':'What Did You Work On?',
                'plan':'What is your next plan of action?',
                'challenge':'What Challenges are you facing?',
                'uploaded' : 'Have you uploaded your assignments to Interview Portal?'
                }
'''
    def __init__(self, **kwargs):
        super(DSUForm, self).__init__(**kwargs)
        self.fields["trained_by"].queryset = CustomerUser.objects.filter(
            # Q(is_admin=True) | Q(is_employee=True)| Q(is_client=True)
            Q(is_client=True)
        )
'''
