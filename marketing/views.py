from django.shortcuts import render

# Create your views here.
import requests
import urllib.request
import json
from datetime import datetime,date,timedelta
from django.db.models import Min,Max
from django.http import JsonResponse,Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render,get_object_or_404
from dateutil.relativedelta import relativedelta
from coda_project import settings
from management.models import Whatsapp,Advertisement
# from .utils import runwhatsapp
from .forms import WhatsappForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
        CreateView,
        DeleteView,
        ListView,
        DetailView,
        UpdateView,
    )
from django.contrib.auth import get_user_model
User=get_user_model()

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
        return reverse("main:whatsapp_list")

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
    return redirect('main:whatsapp_list')

def whatsapp_apis(request):
    whatsaapitems=Whatsapp.objects.all()
    context={
            "whatsaapitems":whatsaapitems
    }
    return render(request, 'main/snippets_templates/marketing/whatsapplist.html',context)

def runwhatsapp(request):
    print("Print this")
    whatsapp_items = Whatsapp.objects.all()

    # Get a list of all group IDs from the Whatsapp model
    group_ids = list(whatsapp_items.values_list('group_id', flat=True))

    # Get the image URL and message from the first item in the Whatsapp model
    image_url = whatsapp_items[0].image_url
    message = whatsapp_items[0].message
    product_id = whatsapp_items[0].product_id
    screen_id = whatsapp_items[0].screen_id
    token = whatsapp_items[0].token

    # Loop through all group IDs and send the message to each group
    for group_id in group_ids:
        print("Sending message to group", group_id)

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
        if response.status_code != 200:
            return response
    return redirect('marketing:whatsapp_status')

def whatsapp_status(request):
    title = 'WHATSAPP'
    response = runwhatsapp(request)
    print(response)
    if response.status_code == 200:
        message = f"Hi, {request.user}, your messages have been sent to your groups."
    else:
        message = f"Hi, {request.user}, your messages have not been sent to your groups"
    context = {"title": title, "message": message}
    return render(request, "main/errors/generalerrors.html", context)


'''
@login_required(login_url="/admin/")
def store_home(request):
    return render(request,"store/home.html")



class CategoriesListView(ListView):
    model=Categories
    template_name="store/products/category_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=Categories.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=Categories.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(CategoriesListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Categories._meta.get_fields()
        return context


class CategoriesCreate(SuccessMessageMixin,CreateView):
    model=Categories
    success_message="Category Added!"
    fields="__all__"
    template_name="store/products/category_create.html"

class CategoriesUpdate(SuccessMessageMixin,UpdateView):
    model=Categories
    success_message="Category Updated!"
    fields="__all__"
    template_name="store/products/category_update.html"


class SubCategoriesListView(ListView):
    model=SubCategories
    template_name="store/products/sub_category_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=SubCategories.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=SubCategories.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(SubCategoriesListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=SubCategories._meta.get_fields()
        return context

class SubCategoriesCreate(SuccessMessageMixin,CreateView):
    model=SubCategories
    success_message="Sub Category Added!"
    fields="__all__"
    template_name="store/products/sub_category_create.html"

class SubCategoriesUpdate(SuccessMessageMixin,UpdateView):
    model=SubCategories
    success_message="Sub Category Updated!"
    fields="__all__"
    template_name="store/products/sub_category_update.html"




#====================ecomerce old===========================

from django.shortcuts import get_object_or_404, render
from .models import Category, Product

def categories(request):
    return {
        'categories': Category.objects.all()
    }

def all_products(request):
    products = Product.products.all()
    return render(request, 'store/home.html', {'products': products})

def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/products/subcategory.html', {'product': product})
'''


