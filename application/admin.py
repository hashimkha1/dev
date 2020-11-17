from django.contrib import admin
from .models import Applicant_Profile,Application,Rated,Employee
# Register your models here.
admin.site.register(Applicant_Profile)
admin.site.register(Application)
admin.site.register(Rated)
#admin.site.register(Uploads)
admin.site.register(Employee)
