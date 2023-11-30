from django import forms
from django.forms import ModelForm, Textarea
# from management.models import Whatsapp,Whatsapp_Groups
from marketing.models import Ads,Whatsapp_Groups
from django.utils.translation import gettext_lazy as _


class WhatsappForm(forms.ModelForm):
    class Meta:
        model = Whatsapp_Groups #Whatsapp
        fields = [
                    "group_name",
                    "group_id",
                    # "image_url",
                    # "message",
                    # "link",
                    "type",
                    # "product_id",
                    # "screen_id",
                    # "token",
        ]
        labels = {
                    "group_name":"Enter Whatsapp Group",
                    "group_id ":"Enter Whatsapp Group id",
                    # "image_url":"Enter url Image",
                    # "message":"Describe the message to be posted",
                    # "link":"Enter link",
                    "type":"ad_type",
                    # "product_id ":"Enter Product ID",
                    # "screen_id":"Enter Screen ID",
                    # "token":"Enter token",
        }

class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads #Whatsapp
        fields = [
                    # "group_name",
                    # "group_id",
                    "image_name",
                    "message",
                    "link",
                    # "type",
        ]
        labels = {
                    # "group_name":"Enter Whatsapp Group",
                    # "group_id ":"Enter Whatsapp Group id",
                    "image_name":"Select image_name",
                    "message":"Describe the message to be posted",
                    "link":"Enter link",
                    # "type":"ad_type",
        }
