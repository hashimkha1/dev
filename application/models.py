# # from coda_project.application.views import first_interview
from datetime import datetime
# from distutils.command.upload import upload
from django.db import models
from django.utils import timezone
# from accounts.models import CustomerUser
# from main.models import Assets
# from django.db.models import Q
# from coda_project.storage import GoogleDriveStorage

class WCAG_GAC_LTD(models.Model):
    website_url = models.CharField(max_length=500)
    page_name = models.CharField(max_length=500)
    improvements = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
