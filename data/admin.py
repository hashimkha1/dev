from django.contrib import admin

from .models import InterviewUpload, Upload

# Register your models here.

admin.site.register(Upload)

admin.site.register(InterviewUpload)