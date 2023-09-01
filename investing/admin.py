from django.contrib import admin
from .models import (
	Liquidity,
	Unusual_Volume,
	credit_spread,
	ShortPut,
	covered_calls,
    Investments,
    Investment_rates,
    Investor_Information
)

# Register your models here.
admin.site.register(Liquidity)
admin.site.register(Unusual_Volume)
admin.site.register(credit_spread)
admin.site.register(ShortPut)
admin.site.register(covered_calls)
admin.site.register(Investments)
admin.site.register(Investment_rates)
admin.site.register(Investor_Information)

