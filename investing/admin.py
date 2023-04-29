from django.contrib import admin
from .models import (
	stockmarket,
	cryptomarket,
	cread_spread,
	ShortPut,
	covered_calls,
)

# Register your models here.
admin.site.register(stockmarket)
admin.site.register(cryptomarket)
admin.site.register(cread_spread)
admin.site.register(ShortPut)
admin.site.register(covered_calls)
