
from django import forms
from django.forms import Textarea


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()