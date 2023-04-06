from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Service)
admin.site.register(Course)
admin.site.register(CourseCategory)
admin.site.register(Assets)

