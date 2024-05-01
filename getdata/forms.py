
from django import forms
from django.forms import Textarea
from getdata.models import OpenaiPrompt



class OpenaiForm(forms.ModelForm):
    class Meta:
        model = OpenaiPrompt
        fields = [
            "category",
            "expert_question" ,
            "role",
            "context_description",
            "clarification_description",
        ]
        # labels = {
        #     "category": "Category",
        #     "prompt": "Client/Staff?",
        #     "context":"First Name",
        #     "role":"Last Name",
        #     "clarifications":"Email",
        # }



class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()