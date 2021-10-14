

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomerUser, Profile


#admin.site.register(CustomerUser)
class CustomerAdmin(UserAdmin):
    add_form=UserCreationForm
    form=UserChangeForm
    list_display=('email','first_name','last_name')


    fieldsets=UserAdmin.fieldsets +(
        (None, {'fields': ('gender','phone','address','city','state','country')}),
    )

    add_fieldsets=UserAdmin.add_fieldsets +(
        (None, {'fields': ('email', 'first_name','last_name','password1','password2','gender','category','phone','address','city','state','country')}),
    )
    search_fields = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(CustomerUser, CustomerAdmin)

# Register your models here.
admin.site.register(Profile)


