from django.contrib import admin

from .models import FeaturedCategory,FeaturedSubCategory, ActivityLinks, FeaturedActivity, Interviews #, DocUpload

'''
# Register your models here.

admin.site.register(DocUpload)
'''
admin.site.register(FeaturedCategory)
admin.site.register(FeaturedSubCategory)
admin.site.register(FeaturedActivity)
admin.site.register(ActivityLinks)
admin.site.register(Interviews)
