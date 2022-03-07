from django.contrib import admin

from .models import  InterviewUpload, DocUpload

# Register your models here.

admin.site.register(DocUpload)

admin.site.register(InterviewUpload)