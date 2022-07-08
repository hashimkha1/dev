from django.contrib import admin

# Register your models here.
from .models import  Payment_History,Default_Payment_Fees,Payment_Information #, DocUpload


admin.site.register(Payment_History)
admin.site.register(Payment_Information)
admin.site.register(Default_Payment_Fees)