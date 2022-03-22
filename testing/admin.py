from django.contrib import admin

from testing.models import Categories, SubCategories,Cat

# Register your models here.
admin.site.register(Categories)
admin.site.register(Cat)
admin.site.register(SubCategories)
