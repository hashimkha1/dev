from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Application,Rated,InteviewUploads,Employee,FirstUpload,Policy,Reporting


class ApplicationForm(UserCreationForm):
    pass
    #email = forms.EmailField()

    #class Meta:
        #model = User
        #model=Application
        #fields = ['first_name','last_name','username', 'email', 'password1', 'password2']

class ApplicantForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Application
        fields = ['id','first_name','last_name','username','phone', 'email','country','resume']
        labels={
                'first_name':'First Name',
                'last_name':'Last Name',
                'username':'User Name',
                'email':'Email',
        }
        '''
    def __init__(self, *args, **kwargs):
        super(ApplicantForm,self).__init__(*args, **kwargs)
        self.fields['gender'].empty_label= "Select"
'''
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rated
        fields = ['id','first_name','last_name','topic', 'punctuality','communication','understanding']
        labels={
                'first_name':'First Name',
                'last_name':'Last Name',
                'topic':'Topic',
                'punctuality':'Punctuality',
                'communication':'Communication',
                'understanding':'Understanding',

        }
        
    def __init__(self, *args, **kwargs):
        super(RatingForm,self).__init__(*args, **kwargs)
        self.fields['punctuality'].empty_label= "Select"
        self.fields['communication'].empty_label= "Select"
        self.fields['understanding'].empty_label= "Select"
        self.fields['topic'].required= False

class InterviewUploadForm(forms.ModelForm):
    class Meta:
        model = InteviewUploads
        fields = ['username','ppt','report','workflow', 'proc','other']
        labels={
                'ppt':'Powerpoint',
                'report':'Tableau Reports',
                'workflow':'Alteryx Workflow',
                'proc':'SQL Script',
                'other':'Other Documents',
        }
        
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['id','first_name','last_name','topic', 'punctuality','communication','understanding','rated_by']
        labels={
                'first_name':'First Name',
                'last_name':'Last Name',
                'topic':'Topic',
                'punctuality':'Punctuality',
                'communication':'Communication',
                'understanding':'Understanding',
                'rated_by':'Rated_By',
        }
        
    def __init__(self, *args, **kwargs):
        super(EmployeeForm,self).__init__(*args, **kwargs)
        self.fields['punctuality'].empty_label= "Select"
        self.fields['communication'].empty_label= "Select"
        self.fields['understanding'].empty_label= "Select"
        self.fields['topic'].required= False

class InterviewForm(forms.ModelForm):
    class Meta:
        model = FirstUpload
        fields = ['username','first_name','last_name','ppt','report','workflow', 'proc']
        labels={
                'username':'User Name',
                'first_name':'First Name',
                'last_name':'Last Name',
                'ppt':'Powerpoint',
                'report':'Tableau Reports',
                'workflow':'Alteryx Workflow',
                'proc':'SQL Script',

                }
            
class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['first_name','last_name','policy_type','description','policy_doc']
        labels={
                'first_name':'First Name',
                'last_name':'Last Name',
                'policy_type':'Policy Type',
                'description':'Description',
                'policy_doc':'Attach Policy',
                }

class ReportingForm(forms.ModelForm):
    class Meta:
        model = Reporting
        fields = ['first_name','last_name','method','interview_type']
        labels={
                'first_name':'First Name',
                'last_name':'Last Name',
                'gender' :'Gender',
                'method':'Method',
                'interview_type':'Interview Type',
                'reporting_date':'Reporting Date',
                }
