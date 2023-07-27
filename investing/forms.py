from django import forms
from .models import Investments,Investment_rates,stockmarket,ShortPut,covered_calls,credit_spread,cryptomarket
from .models import ShortPut

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investments
        fields = "__all__"

class InvestmentRateForm(forms.ModelForm):
    class Meta:
        model = Investment_rates
        fields = "__all__"
        
class CoveredCallsForm(forms.ModelForm):
    class Meta:
        model = covered_calls
        # fields = "__all__"
        fields = ['symbol','comment','is_featured']


class ShortPutForm(forms.ModelForm):
    class Meta:
        model = ShortPut
        # fields = '__all__'
        fields = ['symbol','comment','is_featured']

class CreditSpreadForm(forms.ModelForm):
    class Meta:
        model = credit_spread
        # fields = "__all__"
        fields = ['symbol','comment','is_featured']