from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import work_department,codawcags

# # Register your models here.
# admin.site.register(UserProfile)
# admin.site.register(Application)
# admin.site.register(Rated)
admin.site.register(codawcags)
admin.site.register(work_department)
