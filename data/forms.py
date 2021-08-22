from django import forms
from .models import InterviewUpload


class InterviewForm(forms.ModelForm):
    class Meta:
        model = InterviewUpload
        fields = ['first_name','last_name','category','question_type','doc','link']
        labels={
                'first_name':'First Name',
                'last_name':'Last Name',
                'category':'Category',
                'question_type':'Question',
                'doc':'Assignment',
                'link':'Google Share Url',
                }


