from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import (
            Employee,
            Department,
            Category,
            Activity,
            Transaction
)
''' 
class EmployeeInline(admin.TabularInline):
    model=Employee

admin.site.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    inlines=[
        EmployeeInline,
    ]

class ActivityInline(admin.TabularInline):
    model=Activity

admin.site.register(Category,MPTTModelAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    inlines=[
        ActivityInline,
    ]

'''
# Register your models here.
admin.site.register(Employee)

admin.site.register(Transaction)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category,MPTTModelAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

'''
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
'''

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_name','description', 'point','mx_point', 'mx_earning','created']
    list_filter = ['activity_name', 'is_active']
    list_editable = ['description', 'point','mx_point','mx_earning']
    prepopulated_fields = {'slug': ('activity_name',)}

  
