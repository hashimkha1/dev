import os,requests
import json
# from django.core.management import call_command
from django.db.models import Q
from django.db.models import IntegerField, F,Sum
from django.db.models.functions import Cast
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from marketing.models import Ads,Whatsapp_Groups,Whatsapp_dev
from coda_project import settings
from .forms import WhatsappForm,AdsForm
from django.urls import reverse
from mail.custom_email import send_email
from main.utils import path_values,courses
from getdata.utils import Run_Command
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

#====================AD MANAGEMENT===========================
class AdsCreateView(LoginRequiredMixin, CreateView):
    model = Ads
    success_url = "marketing/adslist/"  
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

@login_required
def delete_ads(request,id):
    ad = Ads.objects.get(pk=id)
    if request.user.is_superuser:
        ad.delete()
    return redirect('marketing:ads_list')

@login_required
def ads(request):
    ad_items=Ads.objects.all()
    context={
            "ad_items":ad_items
    }
    return render(request, 'marketing/adlist.html',context)

#====================WHATSAPP MANAGEMENT===========================
class whatsappCreateView(LoginRequiredMixin, CreateView):
    model = Whatsapp_Groups
    success_url = "/marketing/whatsapplist/"  
    form_class=WhatsappForm
    # fields = "__all__"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class whatsappUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Whatsapp_Groups
    form_class = WhatsappForm

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Replace 'all' with the appropriate title value you need to pass
        return reverse("marketing:whatsapp_list", kwargs={'title': 'all'})

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        elif self.request.user:
            return True
        return False


@login_required
def delete_whatsapp(request,slug):
    whatsapp_record = Whatsapp_Groups.objects.get(pk=slug)
    if request.user.is_superuser:
        whatsapp_record.delete()
    return redirect('marketing:whatsapp_list')

# @login_required
# def whatsapp_groups(request,title):
#     # Extract necessary path information and subtitles for page context
#     path_list, sub_title, pre_sub_title = path_values(request)
#     # Fetch active groups and total participant count if the subtitle indicates 'active_groups'
#     if title == 'active_groups':
#         whatsapp_groups = Whatsapp_Groups.objects.filter(is_active=True)
#         participant_count_filter = {'is_active': True}

#     elif title == 'featured_groups':
#         whatsapp_groups = Whatsapp_Groups.objects.filter(is_featured=True)
#         participant_count_filter = {'is_featured': True}

#     elif title == 'silver':
#         whatsapp_groups = Whatsapp_Groups.objects.filter(is_featured=True)
#         participant_count_filter = {'is_featured': True}

#     elif title == 'basic':
#         whatsapp_groups = Whatsapp_Groups.objects.filter(is_featured=True)
#         participant_count_filter = {'is_featured': True}

#     else:
#         # For any other subtitle, fetch all groups and order by participant count
#         whatsapp_groups = Whatsapp_Groups.objects.annotate(
#             participant_count=Cast('participants', IntegerField())
#         ).order_by('-participant_count')
#         participant_count_filter = {}

#     # Calculate the total participants across all fetched groups
#     total_participants = whatsapp_groups.aggregate(
#         total=Sum(Cast('participants', IntegerField()))
#     )['total']
    
#     # Prepare the context data for rendering
#     print(whatsapp_groups)
#     context = {
#         "whatsapp_items": whatsapp_groups,
#         "total_participants": total_participants
#     }
    
#     return render(request, 'marketing/groups.html', context)


# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.db.models import IntegerField, Sum, Case, When, Value
# from .models import Whatsapp_Groups

# @login_required
# def whatsapp_groups(request, title):
#     # Fetch groups based on title
#     if title == 'active_groups':
#         whatsapp_groups = Whatsapp_Groups.objects.filter(is_active=True)
#         participant_count_filter = {'is_active': True}

#     elif title == 'featured_groups':
#         whatsapp_groups = Whatsapp_Groups.objects.filter(is_featured=True)
#         participant_count_filter = {'is_featured': True}

#     elif title == 'silver':
#         # Filter groups with participant count between 150 and 500
#         whatsapp_groups = Whatsapp_Groups.objects.annotate(
#             participant_count=Cast('participants', IntegerField())
#         ).filter(participant_count__gte=150, participant_count__lte=500)

#     elif title == 'basic':
#         # Filter groups with participant count less than 150
#         whatsapp_groups = Whatsapp_Groups.objects.annotate(
#             participant_count=Cast('participants', IntegerField())
#         ).filter(participant_count__lt=150)

#     else:
#         # Default case: Fetch all groups and order by participant count
#         whatsapp_groups = Whatsapp_Groups.objects.annotate(
#             participant_count=Cast('participants', IntegerField())
#         )

#     # Calculate the total participants across all fetched groups
#     total_participants = whatsapp_groups.aggregate(
#         total=Sum('participant_count')
#     )['total'] if whatsapp_groups else 0
    
#     # Prepare the context data for rendering
#     context = {
#         "whatsapp_items": whatsapp_groups.order_by('-participants'),
#         "total_participants": total_participants
#     }
    
#     return render(request, 'marketing/groups.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import IntegerField, Sum, Case, When, Value
from .models import Whatsapp_Groups

@login_required
def whatsapp_groups(request, title):
    # Annotate groups with participant count
    annotated_whatsapp_groups = Whatsapp_Groups.objects.annotate(
        participant_count=Cast('participants', IntegerField())
    )

    # Fetch groups based on title
    if title == 'active_groups':
        whatsapp_groups = annotated_whatsapp_groups.filter(is_active=True)

    elif title == 'featured_groups':
        whatsapp_groups = annotated_whatsapp_groups.filter(is_featured=True)

    elif title == 'silver':
        # Filter groups with participant count between 150 and 500
        whatsapp_groups = annotated_whatsapp_groups.filter(participant_count__gte=150, participant_count__lte=500)

    elif title == 'basic':
        # Filter groups with participant count less than 150
        whatsapp_groups = annotated_whatsapp_groups.filter(participant_count__lt=150)

    else:
        # Default case: Fetch all groups and order by participant count
        whatsapp_groups = annotated_whatsapp_groups

    # Calculate the total participants across all fetched groups
    total_participants = whatsapp_groups.aggregate(total=Sum('participant_count'))['total'] if whatsapp_groups else 0
    
    # Prepare the context data for rendering
    context = {
        "whatsapp_items": whatsapp_groups.order_by('-participant_count'),
        "total_participants": total_participants
    }
    return render(request, 'marketing/groups.html', context)


# @login_required
# def whatsapp_groups(request):
#     whatsapp_groups = Whatsapp_Groups.objects.annotate(
#     participant_count=Cast('participants', IntegerField())).order_by('-participant_count')
#     total_participants = Whatsapp_Groups.objects.aggregate(
#     total=Sum(Cast('participants', IntegerField()))
#     )['total']
#     context={
#             "whatsaapitems":whatsapp_groups,
#             "total_participants":total_participants
#     }
#     return render(request, 'marketing/groups.html',context)

# @login_required
# def whatsapp_groups(request):
#     # whatsaapitems=Whatsapp_Groups.objects.all().order_by('participants')
#     whatsapp_groups = Whatsapp_dev.objects.annotate(
#     participant_count=Cast('participants', IntegerField())).order_by('-participant_count')
#     total_participants = Whatsapp_dev.objects.aggregate(
#     total=Sum(Cast('participants', IntegerField()))
#     )['total']
#     print(total_participants)
#     context={
#             "whatsaapitems":whatsapp_groups,
#             "total_participants":total_participants
#     }
#     return render(request, 'marketing/groups.html',context)


@login_required(login_url="accounts:account-login")
def refresh_whatsapp_groups(request):
    # Trigger the management command
    if request.user.is_superuser:
        Run_Command('fetch_whatsapp_groups')
        return redirect('marketing:whatsapp_list')
    else:
        return redirect('marketing:whatsapp_list')

# @login_required(login_url="accounts:account-login")
# def refresh_whatsapp_groups(request):
#     Run_Command('fetch_whatsapp_groups')
#     return redirect('marketing:whatsapp_list')


@login_required(login_url="accounts:account-login")
def runwhatsapp(request):
    product_id = os.environ.get('MAYTAPI_PRODUCT_ID')
    screen_id = os.environ.get('MAYTAPI_SCREEN_ID')
    token = os.environ.get('MAYTAPI_TOKEN')
    title = 'WHATSAPP'
    ads_items = Ads.objects.filter(is_active=True, image_name__is_active=True)
    for ad in ads_items:
        whatsapp_groups = Whatsapp_Groups.objects.filter(type=ad.image_name.category,is_active=True)
        group_ids = list(whatsapp_groups.values_list('group_id', flat=True))
        image_url = ad.image_name.image_url
        full_image__url=f'http://drive.google.com/uc?export=view&id={image_url}'
        message = ad.message
        company_description = ad.bulletin if ad.bulletin else ''
        link = ad.link
        # topic=ad.ad_title if ad.ad_title else 'General'
        topic=ad.bulletin if ad.bulletin else 'General'
        company=ad.company if ad.company else 'CROWN DATA ANALYSIS & CONSULTING LLC'
        short_name=ad.short_name if ad.short_name else 'CODA'
        signature=ad.signature if ad.signature else 'Chris Maghas-AI|Automation Expert'
        company_site=ad.company_site if ad.signature else 'www.codanalytics.net/accounts/join'
        video_link= f"Here is the recorded video:{ad.video_link}.Enjoy!" if ad.video_link else ''
        join_link= f"Join Zoom Meeting \n:{ad.meeting_link}" if ad.meeting_link else ''
        post= f'{company}-{short_name}\n\n{company_description}\n\n{topic}\n\n{message}\n\n{video_link}\n{join_link}\n\nFor questions, please reach us at: {company_site}\n{signature}'
        for group_id in group_ids:
            if image_url:
                message_type = "media"
                message_content = full_image__url
                filename = "image.jpg"

                payload = {
                    "to_number": group_id,
                    "type": message_type,
                    "message": message_content,
                    "text":post #f'{message}\nvisit us at {link}'
                }
            else:
                message_type = "text"
                message_content = post # f'{message}\nvisit us at {link}'
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

            if response.status_code != 200:
                print(f"Error sending message to group {group_id}")

    message = f"Hi, {request.user}, this post {post} have been sent to your groups."
    context = {"title": title, "message": message}
    return render(request, "main/errors/generalerrors.html", context)


# @login_required(login_url="accounts:account-login")
# def runwhatsapp(request):
#     product_id = os.environ.get('MAYTAPI_PRODUCT_ID')
#     screen_id = os.environ.get('MAYTAPI_SCREEN_ID')
#     token = os.environ.get('MAYTAPI_TOKEN')
#     title = 'WHATSAPP'

#     ads_items = Ads.objects.filter(is_active=True).prefetch_related('image_name')
#     for ad in ads_items:
#         whatsapp_groups = Whatsapp_Groups.objects.filter(type=ad.image_name.category)
#         group_ids = list(whatsapp_groups.values_list('group_id', flat=True))

#         message_payload = build_message_payload(ad)

#         for group_id in group_ids:
#             send_message(product_id, screen_id, token, group_id, message_payload)

#     messages.success(request, "Your messages have been sent to your groups.")
#     return render(request, "main/errors/generalerrors.html", {"title": title})

def send_email_ads(request):
    path_list,sub_title,pre_sub_title=path_values(request)
    subject='NEXT CLASSES!SIGN UP!'
    url='marketing/marketing_ads.html'
    message=''
    error_message=f'Hi,{request.user.first_name}, there seems to be an issue on our end.kindly contact us directly for payment details.'
    context_data = services(request)
    user_category = request.user.category
    # Retrieve the list of users based on their category
    # users_to_email = User.objects.filter(category=user_category)
    users_to_email = User.objects.filter(is_staff=True,is_active=True)
    # print(users_to_email)
    plans = context_data.get('plans')
    pricing_info = context_data.get('pricing_info')

    context={
                "SITEURL": settings.SITEURL,
                'subtitle': sub_title,
                'user': request.user.first_name,
                "services": plans,
                'services': pricing_info,
                'courses':courses,
                'message':message,
                'error_message':error_message,
                'contact_message':'info@codanalytics.net',
            }
    try:
        # Send email to each user in the selected category
        for user in users_to_email:
            send_email(
                category=user.category,  
                to_email=[user.email],
                subject=subject,
                html_template=url,
                context=context
            )

        return render(request, "marketing/marketing_ads.html", context)
    except Exception as e:
        print(f"An error occurred: {e}")
        return render(request, "marketing/marketing_ads.html", context)
    