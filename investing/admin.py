from django.contrib import admin
from .models import (
	InvestmentContent,
	Ticker_Data,
	credit_spread,
	ShortPut,
	covered_calls,
    Investments,
    Investment_rates,
    Investor_Information,
    Portifolio,
    OverBoughtSold,
    InvestmentsStrategy
)

# Register your models here.
admin.site.register(Ticker_Data)
admin.site.register(Portifolio)
admin.site.register(OverBoughtSold)
admin.site.register(credit_spread)
admin.site.register(ShortPut)
admin.site.register(covered_calls)
admin.site.register(Investments)
admin.site.register(Investment_rates)
admin.site.register(Investor_Information)
admin.site.register(InvestmentContent)
admin.site.register(InvestmentsStrategy)
# class InvestmentContentAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug', 'description')

