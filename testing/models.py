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
