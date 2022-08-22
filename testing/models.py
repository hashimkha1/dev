from django.db.models import Q
from posixpath import basename
import random
import os
import calendar
from decimal import *
from django.forms import CharField
from django.utils.translation import gettext_lazy as _
from sqlite3 import Timestamp
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
import requests
from django.http import request

from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from accounts.models import Tracker
from django.utils import timezone

#User=settings.AUTH_USER_MODEL
User = get_user_model()

class Services(models.Model):
    title = models.CharField(
        max_length=55,
        unique=True,
        default="Group A"
    )
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    price=models.DecimalField(decimal_places=2,max_digits=20,default=39.99)
    # image=models.ImageField(upload_to=upload_image_path,null=True, blank=True)
    image=models.ImageField(upload_to="Uploads/Images/",null=True, blank=True)
    featured=models.BooleanField(default=False)
    active=models.BooleanField(default=True)

    def get_absolute_url(self):
        return "/services/{slug}/".format(slug=self.slug)

    def __str__(self):
        return self.title