from django.contrib import admin
from .models import Picture ,Service, Order,Expenses #,Codadoc ,Codadocuments,Codadocs

# Register your models here.
admin.site.register(Picture)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Expenses)
#admin.site.register(Codadocs)
#admin.site.register(Codadoc)
