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
    LoanUsers,
    Payment_History,
    Default_Payment_Fees,
    Payment_Information,
    Transaction,Inflow,
    TrainingLoan
)  # , DocUpload
from accounts.models import Department

class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "amount")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload-csv/", self.upload_csv),
        ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith(".csv"):
                messages.warning(
                    request, "The wrong file type was uploaded, it should be a csv file"
                )
                return HttpResponseRedirect(request.path_info)

            # file= csv_file.read().decode("utf-8")
            file = csv_file.read().decode("ISO-8859-1")
            file_data = file.split("\n")
            csv_data = [line for line in file_data if line.strip() != ""]
            print(csv_data)
            for x in csv_data:
                fields = x.split(",")
                new_date = datetime.strptime(fields[0], "%m/%d/%Y")
                # idval = Department.objects.values_list("id")[0]
                # dept_id=idval[0]
                department = Department.objects.get_by_id(id=fields[7])
                # idval = Department.objects.values_list("id")[0]
                # department = Department.objects.all().first
                print(department)
                print(new_date)
                created = Transaction.objects.update_or_create(
                    # activity_date=fields[0],
                    activity_date=new_date,
                    # sender=fields[1],
                    sender=request.user,
                    receiver=fields[2],
                    phone=fields[3],
                    qty=fields[4],
                    amount=fields[5],
                    payment_method=fields[6],
                    # department=fields[7],
                    department=department,
                    category=fields[8],
                    type=fields[9],
                    description=fields[10],
                    receipt_link=fields[11],
                )
            url = reverse("admin:index")
            return HttpResponseRedirect(url)
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)

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

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Payment_History, Payment_HistoryAdmin)
admin.site.register(Inflow)
admin.site.register(Payment_Information)
admin.site.register(Default_Payment_Fees)
admin.site.register(TrainingLoan)
admin.site.register(LoanUsers)
