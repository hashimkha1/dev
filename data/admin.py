from django.contrib import admin

from .models import *


class FeaturedSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'title')
    list_editable = ('order',)


class TrainingResponsesTrackingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'featuredsubcategory')
class ActivityLinksAdmin(admin.ModelAdmin):
    list_display = ('link_name',  'Featuredsubcategory')
    
  


admin.site.register(ActivityLinks, ActivityLinksAdmin)
'''
# Register your models here.

admin.site.register(DocUpload)
'''
admin.site.register(FeaturedCategory)
admin.site.register(FeaturedSubCategory, FeaturedSubCategoryAdmin)
admin.site.register(TrainingResponsesTracking, TrainingResponsesTrackingAdmin)
admin.site.register(FeaturedActivity)
admin.site.register(Tool_Catogory)
admin.site.register(Analytics_Tools)
admin.site.register(Training_Responses)
admin.site.register(Interviews)
admin.site.register(Prep_Questions)
admin.site.register(JobRole)
admin.site.register(ClientAssessment)
