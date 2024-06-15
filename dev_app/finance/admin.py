from django.contrib import admin
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime
# dt_string = "12/11/2018 09:15:32"
# Register your models here.
from django.urls import path, reverse
from .models import (
    Payment_History,
    Default_Payment_Fees,
    Payment_Information,
    Transaction,Inflow,Outflow
)  # , DocUpload

class Payment_HistoryAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "payment_fees",
        "down_payment",
        "student_bonus",
        "fee_balance",
        "plan",
        "contract_submitted_date",
    )

admin.site.register(Transaction)
admin.site.register(Payment_History, Payment_HistoryAdmin)
admin.site.register(Inflow)
admin.site.register(Outflow)
admin.site.register(Payment_Information)
admin.site.register(Default_Payment_Fees)

