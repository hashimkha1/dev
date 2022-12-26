from django.http import JsonResponse
from celery import shared_task
from django.shortcuts import redirect, render
from django.views.generic import (
    ListView,
)
import json
from .models import Service
from main.forms import TransactionForm,ContactForm
from main.models import Expenses
from codablog.models import Post
from finance.models import Payment_History, Payment_Information
from management.models import Advertisement
from whatsapp.script import whatsapp
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
# from django.core.management import call_command
import tweepy
import requests
# importing modules
import urllib.request
from PIL import Image
from django.contrib.auth import get_user_model
User=get_user_model()

def error400(request):
    return render(request, "main/errors/400.html", {"title": "400Error"})

def error403(request):
    return render(request, "main/errors/403.html", {"title": "403Error"})

def error404(request):
    return render(request, "main/errors/404.html", {"title": "404Error"})
    
def error500(request):
    return render(request, "main/errors/500.html", {"title": "500Error"})

#Other Error pages or no results error
# def result(request):
#     return render(request, "main/errors/result.html", {"title": "result"})

def general_errors(request):
    # return render(request, "main/errors/noresult.html")
    context={'message':'message'}
    return render(request,'main/errors/generalerrors.html',context)
#  ===================================================================================   
def hendler400(request,exception):
    return render(request, "errors/400.html")

def hendler403(request,exception):
    return render(request, "main/errors/403.html")

def hendler404(request,exception):
    return render(request, "main/errors/404.html")

def hendler404(request,exception):
    return render(request, "main/errors/404.html")

def hendler500(request):
    return render(request, "main/errors/500.html")
    
def test(request):
    return render(request, "main/test.html", {"title": "test"})

def checkout(request):
    return render(request, "main/checkout.html", {"title": "checkout"})

def layout(request):
    # advertisement()
    posts=Post.objects.all()
    context={
            "posts":posts,
            "title": "layout"
        }
    return render(request, "main/home_templates/newlayout.html",context)


def about(request):
    return render(request, "main/about.html", {"title": "about"})


def about_us(request):
    return render(request, "main/home_templates/layout.html", {"title": "about_us"})


def team(request):
    semployees=User.objects.all()
    emps=User.objects.all().filter(is_employee=True)
    staffs=User.objects.all().filter(is_employee=True,is_staff=True)
    context={
        "semployees":semployees,
        "emps":emps,
        "staffs":staffs,
        "title": "team"
    }
    return render(request, "main/team.html",context)


def it(request):
    return render(request, "main/departments/it.html", {"title": "IT"})


def testing(request):
    return render(request, "main/testing.html", {"title": "testing"})
    
def interview(request):
    return redirect('data:interview')
    # return render(request, "main/coach_profile.html", {"title": "coach_profile"})

def coach_profile(request):
    return render(request, "main/coach_profile.html", {"title": "coach_profile"})

@login_required
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("management:assessment")
    else:
        form = ContactForm()
    return render(request, "main/contact.html", {"form": form})


def report(request):
    return render(request, "main/report.html", {"title": "report"})

class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Service
    success_url = "/images/"
    # fields = ["title", "description"]
    fields = ["name", "description","image_url"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        
def images(request):
    # images = Service.objects.all().first()
    images = Service.objects.all()
    print(images)
    return render(request, "main/snippets_templates/static/images.html", {"title": "pay", "images": images})

class ImageUpdateView(LoginRequiredMixin,UpdateView):
    model=Service
    fields = ['name','image_url','description']
     
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:images') 


@login_required
def pay(request):
    try:
        payment_info = Payment_Information.objects.filter(
            customer_id=request.user.id
        ).first()
        return render(request, "main/pay.html", {"title": "pay", "payments": payment_info})
    except:
        message=f'Hi,{request.user}, you are yet to sign the contract with us kindly contact us at info@codanalytics.net'
        link=f'https/www.codanalytics.net/finance/mycontract/{request.user}/'
        link2=f'localhost:8000/finance/mycontract/{request.user}/'
        context={
                  "title": "PAYMENT", 
                  "message": message,
                  "link": link,
                  "link2": link2,

                }
        return render(request, "main/errors/generalerrors.html", context)

def paymentComplete(request):
    payments = Payment_Information.objects.filter(customer_id=request.user.id).first()
    print(payments)
    customer = request.user
    body = json.loads(request.body)
    print("payment_complete:", body)
    payment_fees = body["payment_fees"]
    down_payment = payments.down_payment
    studend_bonus = payments.student_bonus
    plan = payments.plan
    fee_balance = payments.fee_balance
    payment_mothod = payments.payment_method
    contract_submitted_date = payments.contract_submitted_date
    client_signature = payments.client_signature
    company_rep = payments.company_rep
    client_date = payments.client_date
    rep_date = payments.rep_date
    Payment_History.objects.create(
        customer=customer,
        payment_fees=payment_fees,
        down_payment=down_payment,
        student_bonus=studend_bonus,
        plan=plan,
        fee_balance=fee_balance,
        payment_method=payment_mothod,
        contract_submitted_date=contract_submitted_date,
        client_signature=client_signature,
        company_rep=company_rep,
        client_date=client_date,
        rep_date=rep_date,
    )

    return JsonResponse("Payment completed!", safe=False)


def training(request):
    return render(request, "main/training.html", {"title": "training"})


def project(request):
    return render(request, "main/project.html", {"title": "project"})


# -----------------------------Documents---------------------------------
"""
def codadocuments(request):
    codadocuments=Codadoc.objects.all().order_by('-date_uploaded')
    return render(request, 'main/documentation.html', {'codadocuments': codadocuments})


def doc(request):
    if request.method== "POST":
        form=CodadocumentsForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main-documents')
    else:
        form=CodadocumentsForm()
    return render(request, 'main/doc.html',{'form':form})
"""

@shared_task(name="advertisement")
def advertisement():
    """
    This function will post the latest Facebook Ad
    """
    context = Advertisement.objects.all().first()
    # facebook_context = Advertisement.objects.all().first()
    apiKey =context.twitter_api_key # '1zPxZNd57aXHZb8WwQFYEvNbv'  
    apiSecret = context.twitter_api_key_secret # 'UdRcVGDSE9Ntpwz1Rbq3qsGPcYYBCor7Yl6X3wVLR5J6hKczmZ' 
    accessToken = context.twitter_access_token # '1203036386011570177-rgXHzNM25WeUMnua6U13dS7jQmDgWg' 
    accessTokenSecret =context.twitter_access_token_secret #'17cKoLwVdiZMnvKCWSxONCWj1A8atW6OvEAWtpqdUeZLF' 

    # 3. Create Oauth client and set authentication and create API object
    oauth = tweepy.OAuthHandler(apiKey, apiSecret)
    oauth.set_access_token(accessToken, accessTokenSecret)

    api = tweepy.API(oauth)

    # 4. upload media
    # urllib.request.urlretrieve(
    # 'https://drive.google.com/file/d/11X9ZMLnGop3qVoG-vsF9iOd2MpNuwV-M/view?usp=share_link',
    # "advertisement.png")
    urllib.request.urlretrieve(
    'https://media.geeksforgeeks.org/wp-content/uploads/20210318103632/gfg-300x300.png',
    "advertisement.png")
    # image = Image.open("advertisement.png")
    image_path='https://drive.google.com/file/d/11X9ZMLnGop3qVoG-vsF9iOd2MpNuwV-M/view?usp=share_link'
    link = urllib.request.urlopen(image_path).read()
    # image = Image.open(r"https://drive.google.com/file/d/11X9ZMLnGop3qVoG-vsF9iOd2MpNuwV-M/view?usp=share_link") 
    # This method will show image in any image viewer 
    # image.show() 
    # media=googledriveurl={{image.image_url}}
    image=link
    # image='media/profile_pics/Chris.jpg'
    # image='https://drive.google.com/file/d/11X9ZMLnGop3qVoG-vsF9iOd2MpNuwV-M/view?usp=share_link'
    
    
    media = api.media_upload(image)

    api.update_status(
        status=context.post_description,
        # media_ids=[context.tweet_media],
        media_ids=[media.media_id]
    )

    """
        This function will post the latest Facebook Ad
    """

    # facebook_page_id = facebook_context.facebook_page_id
    # access_token = facebook_context.facebook_access_token
    # url = "https://graph.facebook.com/{}/photos".format(facebook_page_id)
    # msg = facebook_context.post_description
    # image_location = facebook_context.image
    # payload = {
    #     "url": image_location,
    #     "access_token": access_token,
    #     "message": msg,
    # }

    # Send the POST request
    # requests.post(url, data=payload)

    

def runwhatsapp(request):
    whatsapp()
    message=f'Hi,{request.user}, your messages have been post to your groups'
    context={
        'title':'WHATSAPP',
        'message':message
    }
    return render (request, "main/errors/generalerrors.html",context)


