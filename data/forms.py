from django import forms
from .models import Upload


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['username','first_name','last_name','doc_type','resume','introduction','project_Story', 'sdlc','environment','performance','testing']
        labels={
                'username':'User Name',
                'first_name':'First Name',
                'last_name':'Last Name',
                'doc_type':'Document Type',
                'resume':'Resume',
                'introduction':'Introduction',
                'project_Story':'Project Story',
                'sdlc':'SDLC',
                'environment':'Environment',
                'performance':'Performance',
                'testing':'Testing',

                }


