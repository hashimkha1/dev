from django import forms
from .models import Investments,Investment_rates,ShortPut,Portifolio

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
    on_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),label="Date")
    class Meta:
        model = ShortPut
        # fields = '__all__'
        fields = ['symbol','comment','on_date','is_featured']

class PortfolioForm(forms.ModelForm):
    # on_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),label="Date")
    user = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    symbol = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    industry = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    action = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))   
    strike_price = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    implied_volatility_rank = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    expiry = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    earnings_date = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    
    class Meta:
        model = Portifolio
        fields = '__all__'
        
        def __init__(self, *args, **kwargs):
            super(PortfolioForm, self).__init__(*args, **kwargs)