from django.contrib import admin

from .models import (
                        FeaturedCategory,FeaturedSubCategory, 
                        ActivityLinks, FeaturedActivity,Interviews, 
                        Training_Responses,Prep_Questions,JobRole
                    )

'''
# Register your models here.

admin.site.register(DocUpload)
'''
admin.site.register(FeaturedCategory)
admin.site.register(FeaturedSubCategory)
admin.site.register(FeaturedActivity)
admin.site.register(Training_Responses)
admin.site.register(ActivityLinks)
admin.site.register(Interviews)
admin.site.register(Prep_Questions)
admin.site.register(JobRole)
