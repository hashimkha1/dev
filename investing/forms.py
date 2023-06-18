from django import forms
from .models import Investments

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investments
        fields = "__all__"

# class UploadForm(forms.ModelForm):
#     class Meta:
#         model = Uploads
#         fields = ['id','doc_type','doc_name','doc','link']
#         labels={
#                 'doc_type':'Document Type',
#                 'doc_name':'Document Name',
#                 'doc':'Document',
#         }
