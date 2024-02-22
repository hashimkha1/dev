# # from coda_project.application.views import first_interview
from datetime import datetime
# from distutils.command.upload import upload

from django.db import models
from django.utils import timezone
# from accounts.models import CustomerUser
# from main.models import Assets
# from django.db.models import Q
# from coda_project.storage import GoogleDriveStorage

#

class Trackerr(models.Model):
    category = models.CharField(max_length=25)
    sub_category = models.CharField(max_length=25)
    task = models.CharField(max_length=25)
    plan = models.CharField(max_length=255)
    empname = models.CharField(max_length=50, null=True)
    author = models.CharField(max_length=50, null=True)
    employee = models.CharField(max_length=255)
    login_date = models.DateTimeField()
    start_time = models.DateTimeField()
    duration = models.IntegerField()
    time = models.PositiveIntegerField()