from django.contrib import admin

# Register your models here.
from .models import (
    Payment_History,
    Default_Payment_Fees,
    Payment_Information,
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


admin.site.register(Payment_History, Payment_HistoryAdmin)
admin.site.register(Payment_Information)
admin.site.register(Default_Payment_Fees)
