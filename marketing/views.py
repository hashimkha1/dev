
import os
from django.shortcuts import render
import requests
import json
from django.db.models import Q
from django.shortcuts import redirect, render
from management.models import Whatsapp,Whatsapp_Groups
from marketing.models import Ads
from main.models import Assets
from .forms import WhatsappForm,AdsForm
from django.urls import reverse
from mail.custom_email import send_email
from main.utils import path_values,courses
from main.context_processors import services
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
        CreateView,
        UpdateView,
    )
from main.context_processors import images
from django.contrib.auth import get_user_model
User=get_user_model()

#====================General===========================
def marketing(request):
    return render(request, "marketing/socialmedia.html", {"title": "Marketing"})
#====================Social Media===========================

class whatsappCreateView(LoginRequiredMixin, CreateView):
    model = Whatsapp_Groups
    success_url = "/whatsapplist/"  
    form_class=WhatsappForm
    # fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class whatsappUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Whatsapp_Groups # Whatsapp 
    form_class=WhatsappForm

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("marketing:whatsapp_list")

    def test_func(self):
        # plan = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user:
            return True
        return False

def delete_whatsapp(request,id):
    whatsapp_record = Whatsapp_Groups.objects.get(pk=id)
    if request.user.is_superuser:
        whatsapp_record.delete()
    return redirect('marketing:whatsapp_list')

def whatsapp_apis(request):
    whatsaapitems=Whatsapp_Groups.objects.all()
    context={
            "whatsaapitems":whatsaapitems
    }
    return render(request, 'marketing/whatsapplist.html',context)


class AdsCreateView(LoginRequiredMixin, CreateView):
    model = Ads
    success_url = "/marketing/adslist/"  
    form_class=AdsForm
    # fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ads # Whatsapp 
    form_class=AdsForm

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("marketing:ads_list")

    def test_func(self):
        # plan = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user:
            return True
        return False

def delete_ads(request,id):
    ad = Ads.objects.get(pk=id)
    if request.user.is_superuser:
        ad.delete()
    return redirect('marketing:ads_list')

def ads(request):
    ad_items=Ads.objects.all()
    context={
            "ad_items":ad_items
    }
    return render(request, 'marketing/adslist.html',context)



def runwhatsapp(request):
    # image_data_analysi_categories = Assets.objects.filter(category='background')
    # image_webdevelopers_categories = Assets.objects.filter(category='webdevelopers')
    # image_Family_categories = Assets.objects.filter(category='Farm')
    # image_investment_categories = Assets.objects.filter(category='Farm')
    # print("image_background===================>",image_investment_categories)

    # Get the environmental variables for product_id,screen and token
    product_id = os.environ.get('MAYTAPI_PRODUCT_ID')
    screen_id = os.environ.get('MAYTAPI_SCREEN_ID')
    token = os.environ.get('MAYTAPI_TOKEN')
    title = 'WHATSAPP'

    # Get the message,image_url,and type from Ads table
    data_url = Ads.objects.filter(image_name__name='data_page_v1').values_list('name', flat=True).first()
    # data_url = Ads.objects.filter(name='data_page_v1').values_list('image_url', flat=True).first()
    image_url =f'http://drive.google.com/uc?export=view&id={data_url}'
    print("images_all===================>",image_url)

   # Get a list of all group IDs from the Whatsapp_Group model
    # whatsapp_items = Whatsapp_Groups.objects.all()
    whatsapp_items = Whatsapp_Groups.objects.filter(group_name='Testing')
    group_ids = list(whatsapp_items.values_list('group_id', flat=True))
    # print("Print this",group_ids)

    # Loop through all group IDs and send the message to each group
    for group_id in group_ids:
        # print("Sending message to group", group_id)
        # Set the message type to "text" or "media" depending on whether an image URL is provided
        if image_url:
            message_type = "media"
            message_content = image_url
            filename = "image.jpg"
        else:
            message_type = "text"
            message_content = message
            filename = None

        # Set up the API request payload and headers
        payload = {
            "to_number": group_id,
            "type": message_type,
            "message": message_content,
            "filename": filename,
        }
        
        headers = {
            "Content-Type": "application/json",
            "x-maytapi-key": token,
        }
        # Send the API request and print the response
        url = f"https://api.maytapi.com/api/{product_id}/{screen_id}/sendMessage"
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        # # Check if the API request was successful
        # if response.status_code != 200:
        #     return response
        # if response.status_code in(200,302,300):
        # print(response)
    
    if response.status_code == 200:
        message = f"Hi, {request.user}, your messages have been sent to your groups."
    else:
        message = f"Hi, {request.user}, your messages have not been sent to your groups"
    context = {"title": title, "message": message}
    return render(request, "main/errors/generalerrors.html", context)
    # return redirect('marketing:whatsapp_status')

# def whatsapp_status(request):
#     title = 'WHATSAPP'
#     response = runwhatsapp(request)
#     print(response)
#     if response.status_code == 200:
#         message = f"Hi, {request.user}, your messages have been sent to your groups."
#     else:
#         message = f"Hi, {request.user}, your messages have not been sent to your groups"
#     context = {"title": title, "message": message}
#     return render(request, "main/errors/generalerrors.html", context)


def send_email_ads(request):
    path_list,sub_title,pre_sub_title=path_values(request)
    subject='NEXT CLASSES!SIGN UP!'
    url='email/marketing/marketing_ads.html'
    message=''
    error_message=f'Hi,{request.user.first_name}, there seems to be an issue on our end.kindly contact us directly for payment details.'
    context_data = services(request)

    # Access the 'plans' variable from the context data
    plans = context_data.get('plans')
    print("plans---->",plans)
    context={
                'subtitle': sub_title,
                'user': request.user.first_name,
                'services':plans,
                'courses':courses,
                'message':message,
                'error_message':error_message,
                'contact_message':'info@codanalytics.net',
            }
    try:
        send_email( category=request.user.category, 
                    to_email=[request.user.email,], 
                    subject=subject, html_template=url, 
		    		context=context
                    )
        return render(request, "email/marketing/marketing_ads.html",context)
    except:
        return render(request, "email/marketing/marketing_ads.html",context)
    