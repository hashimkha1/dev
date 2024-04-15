from django import forms
from .models import InvestmentStrat

class investForm(forms.ModelForm):
    class Meta:
        model = InvestmentStrat
        fields = '__all__'
        widgets = {
            # Add specific widgets if you want to customize the form fields
            # For example, to use a text area for 'comment':
            'comment': forms.Textarea(attrs={'rows': 4}),
            # Add more widgets as needed
        }
