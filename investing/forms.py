from django import forms
from .models import Investments,Investment_rates,ShortPut,Portifolio,InvestmentsStrategy

class InvestmentForm(forms.ModelForm):
    class Meta:
        model =Investments
        fields = ['amount','description']
        # fields = "__all__"

class InvestmentsStrategyForm(forms.ModelForm):
    class Meta:
        model = InvestmentsStrategy
        fields = "__all__"        

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
    # action = forms.CharField(widget=forms.HiddenInput(),)   
    # implied_volatility_rank = forms.CharField(widget=forms.HiddenInput(),)
    earnings_date = forms.CharField(widget=forms.HiddenInput(),)
    symbol = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    industry = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # strike_price = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    condition = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # strategy = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
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
            'implied_volatility_rank',
            'expiry',
            'earnings_date',
            'strategy',
            'long_strike',
            'short_strike',
            'returns',
            'comment',
            # 'amount',
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
        if kwargs.get('initial') and kwargs['initial'].get('create') and kwargs['initial']['create']:
            self.fields['symbol'].widget.attrs['readonly'] = False
            self.fields['industry'].widget.attrs['readonly'] = False
            self.fields['condition'].widget.attrs['readonly'] = False
            self.fields['strategy'].widget.attrs['readonly'] = False
            
            condition_CHOICES = [
                ('neutral','neutral'),
                ('oversold','oversold'),
                ('overbought','overbought')
            ]

            strategy_CHOICES = [
                ('covered_calls', 'covered_calls'),
                ('shortputdata', 'shortputdata'),
                ('credit_spread', 'credit_spread'),
            ]

            # Use ChoiceField in the form
            self.fields['condition'] = forms.ChoiceField(choices=condition_CHOICES,)
            self.fields['strategy'] = forms.ChoiceField(choices=strategy_CHOICES,)
            self.fields['action'].widget = forms.TextInput()
            self.fields['implied_volatility_rank'].widget = forms.TextInput()
            self.fields['earnings_date'].widget = forms.DateInput(attrs={'type': 'date'})