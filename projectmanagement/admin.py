from django.contrib import admin

from .models import Expense, Expenses

# Register your models here.
admin.site.register(Expense)
admin.site.register(Expenses)
