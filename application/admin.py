from django.contrib import admin
from .models import Applicant_Profile,Application,Ratings,InteviewUploads
# Register your models here.
admin.site.register(Applicant_Profile)
admin.site.register(Application)
admin.site.register(Ratings)
admin.site.register(InteviewUploads)