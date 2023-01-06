from django.contrib import admin

from .models import (
    Assets,
    Order,  # ,Codadoc ,Codadocuments,Codadocs
    Picture,
    Service,
    Payments,
)

# Register your models here.
admin.site.register(Picture)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Assets)
# admin.site.register(Codadocs)
# admin.site.register(Codadoc)
admin.site.register(Payments)

