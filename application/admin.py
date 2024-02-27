from django.contrib import admin
from .models import Balance_sheetCategory,BalanceSheetSummary,Balance_Sheet_Entry

# # Register your models here.
# admin.site.register(UserProfile)
# admin.site.register(Application)
admin.site.register(Balance_Sheet_Entry)
admin.site.register(BalanceSheetSummary)
admin.site.register(Balance_sheetCategory)
