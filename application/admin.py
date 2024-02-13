from django.contrib import admin

from .models import (UserProfile, 
                     Application, 
                     Policy, 
                     Rated, 
                     Reporting,Trainee_Assessment,Topic)

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Application)
admin.site.register(Rated)
admin.site.register(Policy)
admin.site.register(Reporting)
admin.site.register(Trainee_Assessment)
admin.site.register(Topic)
