from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (CreateView, DetailView, ListView, UpdateView,
                                  View)

from testing.models import (  # ,CustomUser,MerchantUser,Products,ProductAbout,ProductDetails,ProductMedia,ProductTransaction,ProductTags,StaffUser,CustomerUser
    Categories, SubCategories)


@login_required(login_url="/admin/")
def admin_home(request):
    return render(request,"admin_templates/home.html")

class CategoriesListView(ListView):
    model=Categories
    template_name="admin_templates/category_list.html"
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
    template_name="admin_templates/category_create.html"

class CategoriesUpdate(SuccessMessageMixin,UpdateView):
    model=Categories
    success_message="Category Updated!"
    fields="__all__"
    template_name="admin_templates/category_update.html"


class SubCategoriesListView(ListView):
    model=SubCategories
    template_name="admin_templates/sub_category_list.html"
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
    template_name="admin_templates/sub_category_create.html"

class SubCategoriesUpdate(SuccessMessageMixin,UpdateView):
    model=SubCategories
    success_message="Sub Category Updated!"
    fields="__all__"
    template_name="admin_templates/sub_category_update.html"