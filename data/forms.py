from django import forms

from .models import InterviewUpload, DocUpload


class InterviewForm(forms.ModelForm):
    class Meta:
        model = InterviewUpload
        fields =['category','question_type','doc','link']
        #'first_name','last_name',]
        labels={
                """ 'first_name':'First Name',
                'last_name':'Last Name', """
                'category':'Category',
                'question_type':'Question',
                'doc':'Assignment',
                'link':'Google Share Url',
                }


class UploadForm(forms.ModelForm):
    class Meta:
        model = DocUpload
        fields = ['id','doc_type','doc_name','doc','link']
        labels={
                'doc_type':'Document Type',
                'doc_name':'Document Name',
                'doc':'Document',
        }