from django.contrib import admin
from .models import ReplyMail
from getdata.models import (
	CashappMail,
	ReplyMail,
    Editable,OpenaiPrompt
)

# Register your models here.
admin.site.register(CashappMail)
admin.site.register(ReplyMail)
admin.site.register(Editable)
admin.site.register(OpenaiPrompt)
