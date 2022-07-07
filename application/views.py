from configparser import SectionProxy
import random
import string
from datetime import date, timedelta
from multiprocessing import context
from django.views.decorators.csrf import csrf_exempt

import boto3
from tomlkit import item
from accounts.models import CustomerUser
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.aggregates import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DeleteView, ListView, TemplateView, UpdateView

from .forms import (
    PolicyForm,
    RatingForm,
    ReportingForm,
    ApplicantProfileFormA,
    ApplicantProfileFormB,
    ApplicantProfileFormC,
)
from .models import Applicant_Profile, Application, Policy, Rated, Reporting
from .utils import alteryx_list, dba_list, posts, tableau_list

# User=settings.AUTH_USER_MODEL
User = get_user_model()


def apply(request):
    return redirect("accounts:join")


class ApplicantListView(ListView):
    model = Application
    template_name = (
        "application/applications/applicants.html"  # <app>/<model>_<viewtype>
    )
    context_object_name = "applicants"
    ordering = ["-application_date"]


class application(TemplateView):
    template_name = "application.html"


class ApplicantDeleteView(LoginRequiredMixin, DeleteView):
    model = Application
    template_name = "application/applications/applicants.html"

    def get_success_url(self):
        return reverse("applicant-list")


def applicantlist(request):
    applications = Application.objects.filter().order_by("-application_date")
    applicants = CustomerUser.objects.filter(is_applicant=True).order_by("-date_joined")

    # applicants=User.objects.filter(is_applicant=True).order_by('-date_joined')
    context = {"applications": applications, "applicants": applicants}
    return render(request, "application/applications/applicants.html", context)


"""
class ApplicantDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Application
    success_url='/application/applications/applicants.html'

    def test_func(self):
        applicant = self.get_object()
        if self.request.user == 'admin':
            return True
        return False
"""


@login_required
def applicant_profile(request):
    return render(request, "application/applications/applicant_profile.html")


# def testinterview(request):
#     return render(request, "application/interview_process/firstinterview/sectionB.html")

# ------------------------Interview Section-------------------------------------#.
def career(request):
    return render(request, "application/applications/career.html", {"title": "career"})


@login_required
def interview(request):
    context = {"posts": posts}
    return render(request, "application/interview_process/interview.html", context)


# def first_interview(request):
#     return render(
#         request,
#         "application/interview_process/first_interview.html",
#         {"title": "first_interview"},
#     )
@csrf_exempt
@login_required
def FI_sectionA(request):
    form = ApplicantProfileFormA(
        request.POST, request.FILES, instance=request.user.applicant_profile
    )
    if request.method == "POST":
        form = ApplicantProfileFormA(
            request.POST, request.FILES or None, instance=request.user
        )
        if form.is_valid():
            data = form.cleaned_data["user"] = request.user
            section = data.applicant_profile.section
            if section == "A" or section == "":
                data.applicant_profile.section = "B"
                data.applicant_profile.save()
            form.save()
            return redirect("application:section_b")
    return render(
        request,
        "application/interview_process/firstinterview/sectionA.html",
        {"title": "First Section", "form": form},
    )


@login_required
def FI_sectionB(request):
    form = ApplicantProfileFormB(
        request.POST, request.FILES, instance=request.user.applicant_profile
    )
    if request.method == "POST":
        form = ApplicantProfileFormB(
            request.POST, request.FILES, instance=request.user.applicant_profile
        )
        if form.is_valid():
            data = form.cleaned_data["user"] = request.user
            section = data.applicant_profile.section
            if section == "B":
                data.applicant_profile.section = "C"
                data.applicant_profile.save()
            form.save()
        return redirect("application:section_c")

    return render(
        request,
        "application/interview_process/firstinterview/sectionB.html",
        {"title": "First Section", "form": form},
    )


@login_required
def FI_sectionC(request):
    form = ApplicantProfileFormC(
        request.POST, request.FILES, instance=request.user.applicant_profile
    )
    if request.method == "POST":
        form = ApplicantProfileFormC(
            request.POST, request.FILES, instance=request.user.applicant_profile
        )
        if form.is_valid():
            form.save()
            return redirect("application:policies")

    return render(
        request,
        "application/interview_process/firstinterview/sectionC.html",
        {"title": "First Section", "form": form},
    )


def first_interview(request):
    section = Applicant_Profile.objects.values_list("section", flat=True).get(
        user=request.user
    )

    context = {
        "alteryx_list": alteryx_list,
        "dba_list": dba_list,
        "tableau_list": tableau_list,
        # 'section': section
    }

    return render(
        request, "application/interview_process/first_interview.html", context
    )


def uploadinterviewworks(request):
    print(request.user, request.user.id)
    myfile = request.FILES["myfile"]
    section = request.POST["section"]
    profilename = myfile.name
    extension = str(profilename[profilename.rindex(".") :])
    allowed_extlist = [".zip"]
    if extension not in allowed_extlist:
        return JsonResponse(
            {"success": False, "message": "Invalid file type.Formats allowed: zip."}
        )

    if myfile.size > 50000000:
        context["success"] = False
        context["message"] = "File size sholud be less than 50MB"
        return JsonResponse(context)

    filename = "".join(random.choices(string.digits, k=5))
    des_path = "applicants/interview/" + str(request.user.id) + filename + ".zip"

    s3 = boto3.resource(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    response = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
        Key=des_path, Body=myfile
    )
    print("response", response)
    print("section", section)
    Applicant_Profile.objects.filter(applicant=request.user).update(section=section)
    return JsonResponse({"success": True})


def orientation(request):
    return render(
        request, "application/orientation/orientation.html", {"title": "orientation"}
    )


def internal_training(request):
    return render(
        request,
        "application/orientation/internal_training.html",
        {"title": "orientation"},
    )


def policy(request):
    if request.method == "POST":
        form = PolicyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("application:policies")
    else:
        form = PolicyForm()
    return render(request, "application/orientation/policy.html", {"form": form})




def policies(request):
    reporting_date = date.today() + timedelta(days=7)
    uploads = Policy.objects.all().order_by("upload_date")
    context = {"uploads": uploads, "reporting_date": reporting_date}
    return render(request, "application/orientation/policies.html", context)


class PolicyUpdateView(LoginRequiredMixin, UpdateView):
    model = Policy
    fields = [
        "first_name",
        "last_name",
        "upload_date",
        "method",
        "policy_type",
        "description",
    ]

    form = PolicyForm()

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("application:policies")

    def test_func(self):
        # employee = self.get_object()
        if self.request.is_admin:
            return True
        if self.request.is_superuser:
            return True
        return False


class TraineeDeleteView(LoginRequiredMixin, DeleteView):
    model = Reporting

    def get_success_url(self):
        return reverse("application:trainees")

def info(request):
    reporting_date = date.today() + timedelta(days=7)
    uploads = Policy.objects.all().order_by("upload_date")
    context = {"uploads": uploads, "reporting_date": reporting_date}
    return render(request, "application/orientation/applicant_info.html", context)


# -------------------------rating Section-------------------------------------#
def rate(request):
    if request.method == "POST":
        form = RatingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("application-rating")
    else:
        form = RatingForm()
    return render(request, "application/orientation/rate.html", {"form": form})


def rating(request):
    ratings = Rated.objects.all().order_by("-rating_date")
    total_punctuality = Rated.objects.all().aggregate(Sum("punctuality"))
    total_communication = Rated.objects.all().aggregate(Sum("communication"))
    total_understanding = Rated.objects.all().aggregate(
        Total_Understanding=Sum("understanding")
    )
    context = {
        "ratings": ratings,
        "total_punctuality": total_punctuality,
        "total_communication": total_communication,
        "total_understanding": total_understanding,
    }
    return render(request, "application/orientation/rating.html", context)


# -------------------------rating Section-------------------------------------#
def trainee(request):
    if request.method == "POST":
        form = ReportingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("application:trainees")
    else:
        form = ReportingForm()
    return render(request, "application/orientation/trainee.html", {"form": form})


def trainees(request):
    trainees = Reporting.objects.all().order_by("-update_date")
    return render(
        request, "application/orientation/trainees.html", {"trainees": trainees}
    )


class TraineeUpdateView(LoginRequiredMixin, UpdateView):
    model = Reporting
    fields = [
        "first_name",
        "last_name",
        "gender",
        "reporting_date",
        "method",
        "interview_type",
        "comment",
    ]
    form = ReportingForm()

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("application:trainees")

    def test_func(self):
        employee = self.get_object()
        if self.request.firstname == employee.name:
            return True
        return False


class TraineeDeleteView(LoginRequiredMixin, DeleteView):
    model = Reporting

    def get_success_url(self):
        return reverse("application:trainees")


# ============JQUERY IMPLEMENTATION======================================
"""
# -------------------------Uploads Section-------------------------------------#
def firstupload(request):
    if request.method== "POST":
        form=InterviewForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application-second_interview')
    else:
        form=InterviewForm()
    return render(request, 'application/interview_process/firstupload.html',{'form':form})

def fupload(request):
    iuploads=FirstUpload.objects.all().order_by('-upload_date')
    return render(request, 'application/interview_process/fupload.html', {'iuploads': iuploads})

def applicants(request):
    return render(request, 'application/applications/applicants.html')
  
def get_total(request):
    title = 'All Applicants'
    queryset = Application.objects.all()
    total_earning = Application.objects.aggregate(Sum("mx_earning"))
    context = {
    "title": title,
    "queryset": queryset,
    "total_earning": total_earning,
    }
    return render(request, 'application/table.html', context)


#API data
def ApplicationDataAPI(request):
    data = Application.objects.all().order_by('-application_date')
    dataList = []
    for i in data:
        dataList.append({
                            'id':i.id,
                            'username':i.username,
                            'first_name':i.first_name,
                            'last_name':i.last_name,
                            'phone':i.phone,
                            'submitted':i.submitted,
                            'phone':i.phone,
                            'country':i.country,
                         })
    
    return JsonResponse(dataList, safe=False)

@csrf_exempt
def updateApplication(request):
    objId = request.POST.get('id')
    point = request.POST.get('point')
    application = Application.objects.get(id=objId)
    application.point = point
    application.save()

    return JsonResponse('Application Updated!', safe=False)

@csrf_exempt
def deleteApplication(request):
	print('Delete called!')
	objId = request.POST.get('id')
	application = Application.objects.get(id=objId)
	application.delete()

	return JsonResponse('Application Deleted!', safe=False)




#============EMPLOYEE IMPLEMENTATION======================================

def employee_form(request,id=0):
    if request.method == "GET":
        if id == 0:
            form=EmployeeForm()
        else:
            employee=Employee.objects.get(pk=id)
            form=EmployeeForm(instance=employee)
        return render(request, 'application/employee_form.html',{'form':form})
    else:
        if id==0:
            form=EmployeeForm(request.POST,request.FILES)
        else:
            employee=Employee.objects.get(pk=id)
            form=EmployeeForm(request.POST,request.FILES,instance=employee)
        if form.is_valid():
            form.save()
        return redirect('application-emp_list')

def employee_insert(request):
    if request.method== "POST":
        form=Employee(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application-update')
    else:
        form=EmployeeForm()
    return render(request, 'application/orientation/rate.html',{'form':form})

def employee_list(request):
    context={'employees': Employee.objects.all().order_by('-punctuality')}
    return render(request, 'application/employee_list.html',context)


def employee_delete(request,id):
    employee = Employee.objects.get(pk=id)
    employee.delete()
    return redirect('application-emp_list')


#------------------------testing Section-----------------------------------------#

def success_stories(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'codablog/success.html', context)
"""
