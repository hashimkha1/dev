from django.contrib import admin
from .models import (
	Ticker_Data,
	credit_spread,
	ShortPut,
	covered_calls,
    Investments,
    Investment_rates,
    Investor_Information,
    Oversold,
    OverBoughtSold
)

# Register your models here.
admin.site.register(Ticker_Data)
admin.site.register(Oversold)
admin.site.register(OverBoughtSold)
admin.site.register(credit_spread)
admin.site.register(ShortPut)
admin.site.register(covered_calls)
admin.site.register(Investments)
admin.site.register(Investment_rates)
admin.site.register(Investor_Information)

