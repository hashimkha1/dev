from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import (
    ListView,
)
import json
from .models import Service
from main.forms import TransactionForm
from main.models import Expenses
from codablog.models import Post
from finance.models import Payment_History, Payment_Information
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
# Create your views here.

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
    return render(request, "main/team.html", {"title": "team"})


def it(request):
    return render(request, "main/departments/it.html", {"title": "IT"})


def testing(request):
    return render(request, "main/testing.html", {"title": "testing"})
    
def interview(request):
    return redirect('data:interview')
    # return render(request, "main/coach_profile.html", {"title": "coach_profile"})

def coach_profile(request):
    return render(request, "main/coach_profile.html", {"title": "coach_profile"})


def contact(request):
    return render(request, "main/contact.html", {"title": "contact"})


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
    payment_info = Payment_Information.objects.filter(
        customer_id=request.user.id
    ).first()
    return render(request, "main/pay.html", {"title": "pay", "payments": payment_info})


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


# -------------------------transactions Section-------------------------------------#
def transact(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("management: management-transaction")
    else:
        form = TransactionForm()
    return render(request, "management/company_finances/transact.html", {"form": form})


""" 
def transaction(request):
    transactions=Expenses.objects.all().order_by('-activity_date')
    return render(request, 'management/company_finances/transaction.html', {'transactions': transactions})
"""


class TransactionListView(ListView):
    model = Expenses
    template_name = "main/transaction.html"  # <app>/<model>_<viewtype>
    context_object_name = "transactions"
    ordering = ["-activity_date"]


"""
class TransactionUpdateView(LoginRequiredMixin,UpdateView):
    model=Expenses
    fields = ['sender','receiver','phone','department', 'category','payment_method','quantity','amount','description','receipt']
     
    def form_valid(self,form):
        form.instance.username=self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('transaction-list') 
"""
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
