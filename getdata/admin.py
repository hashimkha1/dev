from django.contrib import admin
from .models import ReplyMail
from getdata.models import (
	CashappMail,
	ReplyMail,
)

# Register your models here.
admin.site.register(CashappMail)
admin.site.register(ReplyMail)
