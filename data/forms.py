from django import forms
from .models import Interviews #, DocUpload


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