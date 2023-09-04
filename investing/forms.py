from django import forms
from .models import Investments,Investment_rates,ShortPut
from .models import ShortPut

class InvestmentForm(forms.ModelForm):
    class Meta:
        model =Investments
        fields = ['amount','description']
        # fields = "__all__"

class InvestmentRateForm(forms.ModelForm):
    class Meta:
        model = Investment_rates
        fields = "__all__"
        
class OptionsForm(forms.ModelForm):
    class Meta:
        model = ShortPut
        # fields = '__all__'
        fields = ['symbol','comment','is_featured']
