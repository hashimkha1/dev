from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Application,Rated,Uploads


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
        model = Uploads
        fields = ['username']

'''
class InterviewUploadForm(forms.ModelForm):
    class Meta:
        model = Uploads
        fields = ['username','interviewppt','tableau','alteryx', 'SQL','other']
'''