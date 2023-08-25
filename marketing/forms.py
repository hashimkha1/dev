from django import forms
from django.forms import ModelForm, Textarea
from management.models import Whatsapp
from django.utils.translation import gettext_lazy as _


class WhatsappForm(forms.ModelForm):
    class Meta:
        model = Whatsapp
        fields = [
                    "group_name",
                    "group_id",
                    "image_url",
                    "message",
                    "product_id",
                    "screen_id",
                    "token",
        ]
        labels = {
                    "group_name":"Enter Whatsapp Group",
                    "group_id ":"Enter Whatsapp Group id",
                    "image_url":"Enter url Image",
                    "message":"Describe the message to be posted",
                    "product_id ":"Enter Product ID",
                    "screen_id":"Enter Screen ID",
                    "token":"Enter token",
        }
