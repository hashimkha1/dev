from django import forms
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse
from mptt.admin import MPTTModelAdmin
from .models import (
    Requirement,
    Transaction,
    Inflow,
    Outflow,
    Policy,
    Tag,
    Task,
    TaskLinks,
    TaskHistory,
    Twitter,
    Facebook
)

# from .models import Activity, Category, Employee, Transaction , Department

# Register your models here.
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
                created = Transaction.objects.update_or_create(
                    activity_date=fields[0],
                    sender=fields[1],
                    receiver=fields[2],
                    phone=fields[3],
                    qty=fields[4],
                    amount=fields[5],
                    payment_method=fields[6],
                    department=fields[7],
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


admin.site.register(Transaction, TransactionAdmin)

admin.site.register(Inflow)
admin.site.register(Outflow)
admin.site.register(Policy)
admin.site.register(Task)
admin.site.register(TaskHistory)
admin.site.register(Tag)
admin.site.register(Requirement)
admin.site.register(Twitter)
admin.site.register(Facebook)

admin.site.register(TaskLinks)



"""
admin.site.register(Employee)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category,MPTTModelAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_name','description', 'point','mxpoint', 'mxearning']
    list_filter = ['activity_name', 'is_active']
    list_editable = ['description', 'point','mxpoint','mxearning']
    prepopulated_fields = {'slug': ('activity_name',)}

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls
  
    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded, it should be a csv file')
                return HttpResponseRedirect(request.path_info)
            
            #file= csv_file.read().decode("utf-8")
            file= csv_file.read().decode("ISO-8859-1") 
            file_data = file.split("\n")
            csv_data=[line for line in file_data if line.strip() != ""]
            print(csv_data)
             for x in csv_data:
                fields = x.split(",")
                created = Activity.objects.update_or_create(
                                    category=fields[0],
                                    group=fields[1],
                                    activity_name=fields[2],
                                    created_by=fields[3],
                                    description=fields[4],
                                    submission=fields[5],
                                    slug=fields[6],
                                    point=fields[7],
                                    mxpoint=fields[8],
                                    mxearning=fields[9],
                         )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)
           
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)

admin.site.register(Activity, ActivityAdmin)

"""
