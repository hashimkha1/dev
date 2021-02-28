from django import forms
from .models import Document,Uploads

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['id','doc_type','doc_name','doc']
        labels={
                'doc_type':'Document Type',
                'doc_name':'Document Name',
                'doc':'Document',
        }

class UploadForm(forms.ModelForm):
    class Meta:
        model = Uploads
        fields = ['id','doc_type','doc_name','doc','link']
        labels={
                'doc_type':'Document Type',
                'doc_name':'Document Name',
                'doc':'Document',
        }