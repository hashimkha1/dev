from urllib import request
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.template import context
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model,login,authenticate
from django.views.generic import (CreateView,DeleteView,ListView,TemplateView, DetailView,UpdateView)


from .forms import InterviewForm #, UploadForm


from .models import Interview #, DocUpload
from .filters import InterviewFilter #,UserFilter

#User=settings.AUTH_USER_MODEL
User = get_user_model()

def analysis(request):
    return render(request, 'main/home_templates/analysis_home.html', {'title': 'analysis'})

def deliverable(request):
        return render(request, 'data/deliverable/deliverable.html', {'title': 'deliverable'})

@login_required
def training(request):
    return render(request, 'data/training/training.html', {'title': 'training'})

@login_required
def bitraining(request):
    return render(request, 'data/training/bitraining.html', {'title': 'training'})

@login_required
def interview(request):
    return render(request, 'data/interview/interview.html')  

def payroll(request):
    return render(request, 'data/deliverable/payroll.html', {'title': 'payroll'})

def financialsystem(request):
    return render(request, 'data/deliverable/financialsystem.html', {'title': 'financialsystem'})

def project(request):
    return render(request, 'data/deliverable/project.html', {'title': 'project'})

# views on samples reports.
def report(request):
    return render(request, 'data/documents/report.html', {'title': 'report'})
def database(request):
    return render(request, 'data/database.html', {'title': 'report'})

def etl(request):
    return render(request, 'data/etl.html', {'title': 'etl'})  

def getdata(request):
    return render(request, 'data/getdata.html', {'title': 'getdata'}) 

def pay(request):
    return render(request, 'data/pay.html', {'title': 'pay'}) 
# Views on interview Section


@login_required
def uploadinterview(request):
    if request.method== "POST":
        form=InterviewForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('data:iuploads')
    else:
        form=InterviewForm()
    return render(request, 'data/interview/uploadinterview.html',{'form':form})

#for uploading interviews

@login_required
def iuploads(request):
    uploads=Interview.objects.all().order_by('-upload_date')
    myFilter=InterviewFilter(request.GET, queryset=uploads)
    uploads=myFilter.qs
    context={
              'uploads': uploads,
              'myFilter':myFilter
            }
    return render(request, 'data/interview/iuploads.html',context)

def useruploads(request, pk=None, *args, **kwargs):
    useruploads=Interview.objects.filter(author=request.user).order_by('-login_date')
    context = {
                'useruploads': useruploads,
              }
    return render(request, 'data/interview/useruploads.html', context)


@method_decorator(login_required, name='dispatch')
class InterviewDetailView(DetailView):
    model=Interview
    ordering=['-upload_date']


@method_decorator(login_required, name='dispatch')
class InterviewUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Interview
    success_url="/data/interview"
    fields=['user','first_name','last_name','category','question_type''doc','link',]

    def form_valid(self,form):
        #form.instance.author=self.request.user
        if self.request.user.is_superuser:
            return super().form_valid(form)
        else:
            return False

    def test_func(self):
        interview = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user==interview.author:
            return True
        return False
        
@method_decorator(login_required, name='dispatch')
class InterviewDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Interview
    success_url="/data/interview"

    def test_func(self):
        #timer = self.get_object()
        #if self.request.user == timer.author:
        #if self.request.user.is_superuser:
        if self.request.user.is_superuser:
            return True
        return False


# Saving uploaded information to database
'''
def upload(request):
    if request.method== "POST":
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('data-uploaded')
    else:
        form=UploadForm()
    return render(request, 'main/doc_templates/upload.html',{'form':form})


 
def uploaded(request):
    documents=DocUpload.objects.all().order_by('-document_date')
    return render(request, 'main/doc_templates/uploaded.html', {'documents': documents})

'''
