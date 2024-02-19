from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import app_policy,EmployeeProject,company_properties

 # Register your models here.
#admin.site.register(UserProfile)
#admin.site.register(Application)
#admin.site.register(Rated)
admin.site.register(company_properties)
admin.site.register(EmployeeProject)
admin.site.register(app_policy)
