from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import policies,company_resources,work_department,WCAGStandardWebsite

 # Register your models here.
admin.site.register(WCAGStandardWebsite)
admin.site.register(company_resources)
admin.site.register(policies)
#admin.site.register(group_task)
admin.site.register(work_department)
