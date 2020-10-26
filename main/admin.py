from django.contrib import admin
from .models import Picture,Codadoc #,Codadocuments,Codadocs

# Register your models here.
admin.site.register(Picture)
#admin.site.register(Codadocuments)
#admin.site.register(Codadocs)
admin.site.register(Codadoc)
