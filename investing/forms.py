from django import forms
from .models import Investments,stockmarket,ShortPut,covered_calls,cread_spread,cryptomarket
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

class CoveredCallsForm(forms.ModelForm):
    class Meta:
        model = covered_calls
        # fields = "__all__"
        fields = ['Symbol','comment','is_featured']

class ShortPutForm(forms.ModelForm):
    class Meta:
        model = ShortPut
        # fields = "__all__"
        fields = ['Symbol','comment','is_featured']

class CreadSpreadForm(forms.ModelForm):
    class Meta:
        model = cread_spread
        # fields = "__all__"
        fields = ['Symbol','comment','is_featured']