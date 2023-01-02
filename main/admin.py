from django.contrib import admin

from .models import (
    Order,  
    Picture,
    Service,
    Assets,
)

# Register your models here.
admin.site.register(Picture)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Assets)
