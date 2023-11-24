from django.shortcuts import render

# Create your views here.
import requests
import json
from django.db.models import Q
from django.shortcuts import redirect, render
from management.models import Whatsapp
from .forms import WhatsappForm
from django.urls import reverse
from mail.custom_email import send_email
from main.utils import path_values,courses
from main.context_processors import services
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
        CreateView,
        UpdateView,
    )
from django.contrib.auth import get_user_model
User=get_user_model()

#====================General===========================
def marketing(request):
    return render(request, "marketing/socialmedia.html", {"title": "Marketing"})
#====================Social Media===========================

class whatsappCreateView(LoginRequiredMixin, CreateView):
    model = Whatsapp
    success_url = "/whatsapplist/"  
    form_class=WhatsappForm
    # fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class whatsappUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Whatsapp
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
    whatsapp_record = Whatsapp.objects.get(pk=id)
    if request.user.is_superuser:
        whatsapp_record.delete()
    return redirect('marketing:whatsapp_list')

def whatsapp_apis(request):
    whatsaapitems=Whatsapp.objects.all()
    context={
            "whatsaapitems":whatsaapitems
    }
    return render(request, 'marketing/whatsapplist.html',context)

def runwhatsapp(request):
    print("Print this")
    whatsapp_items = Whatsapp.objects.all()

    group_ids = list(whatsapp_items.values_list('group_id', flat=True))
    
    title = 'WHATSAPP'
    image_url = whatsapp_items[0].image_url
    message = whatsapp_items[0].message
    product_id =whatsapp_items[0].product_id   # "c1fbaec3-69c7-4e67-bdab-e69742ffddd0"  #whatsapp_items[1].product_id ""
    screen_id = whatsapp_items[0].screen_id   #"36265" #whatsapp_items[1].screen_id
    token =whatsapp_items[0].token   #"692c55b7-b8ed-471c-a0ef-905df21fe6c7" #whatsapp_items[0].token
    link=whatsapp_items[0].link

    for group_id in group_ids:
        
        if image_url:
            message_type = "media"
            message_content = image_url
            filename = "image.jpg"

            payload = {
                "to_number": group_id,
                "type": "media",
                "message": image_url,
                "text": f'{message}\nvisit us at {link}'
            }
        else:
            message_type = "text"
            message_content = f'{message}\nvisit us at {link}'
            filename = None

            payload = {
                "to_number": group_id,
                "type": message_type,
                "message": message_content,
                "filename": filename,
            }
            
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "x-maytapi-key": token,
        }
        url = f"https://api.maytapi.com/api/{product_id}/{screen_id}/sendMessage"
        response = requests.post(url, headers=headers, data=json.dumps(payload))
       
    if response.status_code == 200:
        message = f"Hi, {request.user}, your messages have been sent to your groups."
    else:
        message = f"Hi, {request.user}, your messages have not been sent to your groups"
    context = {"title": title, "message": message}
    return render(request, "main/errors/generalerrors.html", context)

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
    