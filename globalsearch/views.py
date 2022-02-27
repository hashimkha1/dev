#from tkinter import X
#from xml.dom import xmlbuilder
#from django.db.models import Q
from urllib import request
from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import  redirect, render,get_object_or_404
from django.views.generic import (CreateView,DeleteView,ListView,TemplateView, DetailView,UpdateView)
from data.models import (InterviewUpload)

class SearchInterviewView(ListView):
    template_name="globalsearch/view.html"

    def get_context_data(self, *args,**kwargs):
        context=super(SearchInterviewView,self).get_context_data(*args,**kwargs)
        query=self.request.GET.get('q')
        context['query']=query
        #SearchQuery.objects.create(query=query)
        return context

    def get_queryset(self,*args,**kwargs):
        '''
        __icontains =fields contains this
        __iexact=fields are exactly this
          How do we search on Foreign Keys
        '''
        request=self.request
        print(request.GET)
        method_dict=request.GET
        query=method_dict.get('q',None)
        if query is not None:
            return InterviewUpload.objects.search(query)
        return InterviewUpload.objects.none()
    