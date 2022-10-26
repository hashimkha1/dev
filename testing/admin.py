from django.contrib import admin

from .models import (
    Services,
    # Supplier,
    # Food,
    Logs
)
# Register your models here.
admin.site.register(Services)
# admin.site.register(Supplier)
# admin.site.register(Food)
admin.site.register(Logs)
