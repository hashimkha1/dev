from django.contrib import admin

from .models import (
                        FeaturedCategory,FeaturedSubCategory, 
                        ActivityLinks, FeaturedActivity,Interviews, 
                        Training_Responses,Prep_Questions,JobRole, TrainingResponsesTracking
                    )


class FeaturedSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class TrainingResponsesTrackingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'featuredsubcategory')

'''
# Register your models here.

admin.site.register(DocUpload)
'''
admin.site.register(FeaturedCategory)
admin.site.register(FeaturedSubCategory, FeaturedSubCategoryAdmin)
admin.site.register(TrainingResponsesTracking, TrainingResponsesTrackingAdmin)
admin.site.register(FeaturedActivity)
admin.site.register(Training_Responses)
admin.site.register(ActivityLinks)
admin.site.register(Interviews)
admin.site.register(Prep_Questions)
admin.site.register(JobRole)
