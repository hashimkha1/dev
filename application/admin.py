from django.contrib import admin

from .models import UserProfile, Application, Policy, Rated, Reporting

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Application)
admin.site.register(Rated)
admin.site.register(Policy)
admin.site.register(Reporting)
