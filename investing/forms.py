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
    # user = forms.CharField(widget = forms.HiddenInput(), required = False)
    action = forms.CharField(widget=forms.HiddenInput(),)   
    implied_volatility_rank = forms.CharField(widget=forms.HiddenInput(),)
    earnings_date = forms.CharField(widget=forms.HiddenInput(),)
    symbol = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    industry = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # strike_price = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    condition = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # expiry = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    on_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),label="Date")
    is_active = forms.BooleanField(initial=False,required=False) 
    class Meta:
        model = Portifolio
        # fields = '__all__'    
        fields = [
            'symbol',
            'industry',
            'action',
            'condition',
            'strike_price',
            'implied_volatility_rank',
            'expiry',
            'earnings_date',
            'comment',
            'amount',
            'long_leg_delta',
            'short_leg_delta',
            'long_leg_theta',
            'short_leg_theta',
            'number_of_contract',
            'on_date',
            'is_active',
        ]
        
        def __init__(self, *args, **kwargs):
            super(PortfolioForm, self).__init__(*args, **kwargs)