import calendar
from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
#from .forms import (TransactionForm,OutflowForm,InflowForm,PolicyForm)
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from .models import  Cat,SubCat, Links #,Inflow,Outflow,Policy,Task,Tag

from django.conf import settings
from django.contrib.auth import get_user_model

#User=settings.AUTH_USER_MODEL
User = get_user_model()


def test_home():
    pass

@method_decorator(login_required, name='dispatch')
class CatCreateView(LoginRequiredMixin, CreateView):
    model=Cat
    success_url="/testing/subtest"
    fields=['title','description']

    def form_valid(self,form):
        form.instance.created_by=self.request.user
        return super().form_valid(form)  


@method_decorator(login_required, name='dispatch')
class CatListView(ListView):
    model=Cat
    template_name='testing/subtest.html'
    context_object_name='cats'
    ordering=['-created_at']
    #total_time=Tracker.objects.all().aggregate(Your_Total_Time=Sum('duration'))
  

@method_decorator(login_required, name='dispatch')
class UpdateListView(ListView):
    model=Cat
    template_name='testing/updatelist.html'
    context_object_name='cats'
    ordering=['-updated_at']
    #total_time=Tracker.objects.all().aggregate(Your_Total_Time=Sum('duration'))

    def get_queryset(self):
        """Filter by price if it is provided in GET parameters"""
        queryset = super(UpdateListView, self).get_queryset()
        if 'cat' in self.request.GET:
            queryset = queryset.filter(cat=self.request.GET['price'])
        return queryset


@method_decorator(login_required, name='dispatch')
class CatUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Cat
    success_url="/testing/updatelist"
    fields=['title','description']

    def form_valid(self,form):
        #form.instance.author=self.request.user
        if self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            return False

    def test_func(self):
        cat = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user==cat.created_by:
            return True
        return False

@method_decorator(login_required, name='dispatch')
class CatDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Cat
    success_url="/testing/training_test"

    def test_func(self):
        #timer = self.get_object()
        #if self.request.user == timer.author:
        #if self.request.user.is_superuser:
        if self.request.user.is_superuser:
            return True
        return False

#=====================================SubCategories==========================================

@method_decorator(login_required, name='dispatch')
class SubCatCreateView(LoginRequiredMixin, CreateView):
    model=SubCat
    success_url="/testing/subtest"
    fields=['category','title','description']

    def form_valid(self,form):
        form.instance.created_by=self.request.user
        return super().form_valid(form)  

class SubCatListView(ListView):
    context_object_name = 'home_list'    
    template_name = 'testing/subcatlist.html'
    queryset = SubCat.objects.all()

    def get_context_data(self, **kwargs):
        context = super(SubCatListView, self).get_context_data(**kwargs)
        context['cats'] = Cat.objects.all()
        context['subcats'] = SubCat.objects.all()
        #context['festival_list'] = Festival.objects.all()
        # And so on for more models
        return context

@method_decorator(login_required, name='dispatch')
class SubCatUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=SubCat
    success_url="/testing/updatelist"
    fields=['category','title','description']

    def form_valid(self,form):
        #form.instance.author=self.request.user
        if self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            return False

    def test_func(self):
        cat = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user==cat.created_by:
            return True
        return False
 

""" def cat_subcat(request):
    categories=Cat.objects.prefetch_related('cats')
    context = {
        "categories":categories,
        
    }
    return render(
        request=request,
        template_name='testing/training_test.html',
        context=context
    )
 """
def activity_view(request):
    context = {
        "categories": Cat.objects.prefetch_related('subcat_set').all(),
    }
    return render(request=request, template_name='testing/training_test.html', context=context)

#=====================================Links==========================================

@method_decorator(login_required, name='dispatch')
class LinksCreateView(LoginRequiredMixin, CreateView):
    model=Links
    success_url="/testing/links"
    fields=['subcategory','link_name','link','doc','description']

    def form_valid(self,form):
        form.instance.created_by=self.request.user
        return super().form_valid(form)  


@method_decorator(login_required, name='dispatch')
class LinksUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Links
    success_url="/testing/links"
    fields=['subcategory','doc','link','description','link_name']

    def form_valid(self,form):
        #form.instance.author=self.request.user
        if self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            return False

    def test_func(self):
        cat = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user==cat.created_by:
            return True
        return False
 
class LinksListView(ListView):
    context_object_name = 'home_list'    
    template_name = 'testing/links.html'
    queryset = SubCat.objects.all()


''' 
class TaskDetailSlugView(DetailView):
    queryset=Task.objects.all()
    template_name='management/daf/task_detail.html'
    #ordering = ['-datePosted']

    def get_object(self, *args,**kwargs):
        request=self.request
        slug=self.kwargs.get('slug')
        try:
             instance=Task.objects.get(slug=slug,is_active=True)
        except Task.DoesNotExist:
             raise Http404("User does not exist")

        except Task.MultipleObjectsReturned:
             qs=Task.objects.filter(slug=slug, is_active=True)
             instance= qs.first()
        return instance



class TaskListEmployeeView(ListView):
    queryset=Task.objects.all()
    #user_tasks = User.objects.filter(id=user_id).prefetch_related('taskitem_set')
    template_name='management/daf/employeetask_detail.html'
    #ordering = ['-datePosted']

    def get_object(self, *args,**kwargs):
        request=self.request
        username=self.kwargs.get('user')
        try:
             instance=Task.objects.get(user__username=username,is_active=True)
        except Task.DoesNotExist:
             raise Http404("Task does not exist")
        except Task.MultipleObjectsReturned:
             qs=Task.objects.get(user__username=username,is_active=True)
             instance= qs.first()
        return instance
'''
