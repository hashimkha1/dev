from django.contrib import admin

from .models import Application_Profile, Application, Policy, Rated, Reporting

# Register your models here.
admin.site.register(Application_Profile)
admin.site.register(Application)
admin.site.register(Rated)
admin.site.register(Policy)
admin.site.register(Reporting)
