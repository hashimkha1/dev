from django.contrib import admin

from .models import exception_user,Balancesheet_categories,Balancesheet_category,Balancesheet_entry,BalanceSheet_Summary,items_entry

# # Register your models here.
admin.site.register(Balancesheet_categories)
admin.site.register(Balancesheet_category)
admin.site.register(Balancesheet_entry)
admin.site.register(BalanceSheet_Summary)
admin.site.register(items_entry)
admin.site.register(exception_user)
# admin.site.register(Reporting)
