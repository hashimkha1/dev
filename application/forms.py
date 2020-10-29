from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Application,Rating,InteviewUpload


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
        fields = ['id','first_name','last_name','phone','username', 'email','resume']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['id','first_name','last_name','topic', 'punctuality','communication','understanding']

class InterviewUploadForm(forms.ModelForm):
    class Meta:
        model = InteviewUpload
        fields = ['Interviewid','interviewppt','interviewtab','interviewalteryx', 'interviewdb','interviewother']
