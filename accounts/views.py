from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomerForm
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from .models import CustomerUser
#from django.db.models import Q
# Create your views here.
#---------------Test----------------------
def join(request):
    if request.method== "POST":
        form=CustomerForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('user-login')
    else:
        form=CustomerForm()
    return render(request, 'accounts/join.html', {'form': form})

@login_required
def clients(request):
    #clients=CustomerUser.objects.all().order_by('-date_joined')
    clients=CustomerUser.objects.filter(category = 1)|CustomerUser.objects.filter(category = 2).order_by('-date_joined')
    return render(request, 'accounts/clients.html', {'clients': clients})


