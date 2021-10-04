from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Rated


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rated
        fields = ['first_name','last_name','topic', 'punctuality','communication','understanding']
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

