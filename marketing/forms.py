from django import forms
from marketing.models import Ads,Whatsapp_Groups
from django.utils.translation import gettext_lazy as _


class WhatsappForm(forms.ModelForm):
    class Meta:
        model = Whatsapp_Groups #Whatsapp
        fields = [
                    "group_name",
                    "group_id",
                    "type",
        ]
        labels = {
                    "group_name":"Enter Whatsapp Group",
                    "group_id ":"Enter Whatsapp Group id",
                    "type":"ad_type",
        }


class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads #Whatsapp
        fields = [
                    "image_name",
                    "message",
                    "link",
                    "is_active",
                    "is_featured",
        ]
        labels = {
                    "image_name":"Select image_name",
                    "message":"Describe the message to be posted",
}   