import random
import string
import boto3
from datetime import date, timedelta
from multiprocessing import context
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404,render, redirect
from django.db.models import Q
from accounts.models import CustomerUser
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DeleteView, ListView, TemplateView, UpdateView
from .forms import (
    RatingForm,
    ReportingForm,
    ApplicantProfileFormA,
    ApplicantProfileFormB,
    ApplicantProfileFormC,
)
from .models import UserProfile, Application,Rated, Reporting
from management.models import Policy,Task
from .utils import alteryx_list, dba_list, posts, tableau_list,rewardpoints
from datetime import datetime, timedelta
from main.utils import path_values

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
    path_list,sub_title,pre_sub_title=path_values(request)
    subcategory = CustomerUser.objects.values_list("sub_category",flat=True).filter(sub_category=None)
    print(subcategory)
    coda_applicants = CustomerUser.objects.filter(
        category=1,
        sub_category=None,
        is_applicant=True,
        is_active=True
        ).order_by("-date_joined")
    dck_applicants = CustomerUser.objects.filter(
        category=4,
        sub_category=6,
        is_applicant=True,
        is_active=True
        ).order_by("-date_joined")
    applicants_context = {
             "sub_title": sub_title,
             "applicants": coda_applicants
         }
    dck_context = {
             "sub_title": sub_title,
             "applicants": dck_applicants
         }
    
    if sub_title=='applicants':
        return render(request, "application/applications/applicants.html", applicants_context)
    if sub_title=='dckmembers':
        return render(request, "application/applications/applicants.html",  dck_context)


# ------------------------Interview Section-------------------------------------#.
def career(request):
    return render(request, "application/applications/career.html", {"title": "career"})


@login_required
def interview(request):
    context = {"posts": posts}
    return render(request, "application/interview_process/interview.html", context)


def firstinterview(request):
    return render(
        request,
        "application/interview_process/firstinterview.html",
        {"title": "first_interview"},
    )


@csrf_exempt
@login_required
def FI_sectionA(request):
    form = ApplicantProfileFormA(
        request.POST, request.FILES, instance=request.user.profile
    )

    if request.method == "POST":
        form = ApplicantProfileFormA(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            data = form.cleaned_data["user"] = request.user
            section = data.profile.section
            if section == "A":
                data.profile.section = "B"
                data.profile.save()
            form.save()
            subject = "Interview Message"
        return redirect("application:ratewid", pk="Alteryx")

    return render(
        request,
        "application/interview_process/firstinterview/sectionA.html",
        {"title": "First Section", "form": form},
    )


@login_required
def FI_sectionB(request):
    form = ApplicantProfileFormB(
        request.POST, request.FILES, instance=request.user.profile
    )
    if request.method == "POST":
        form = ApplicantProfileFormB(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            data = form.cleaned_data["user"] = request.user
            section = data.profile.section
            if section == "B":
                data.profile.section = "C"
                data.profile.save()
            form.save()
            subject = "Interview Message"
        return redirect("application:ratewid", pk="Tableau")

    return render(
        request,
        "application/interview_process/firstinterview/sectionB.html",
        {"title": "First Section", "form": form},
    )


@login_required
def FI_sectionC(request):
    form = ApplicantProfileFormC(
        request.POST, request.FILES, instance=request.user.profile
    )
    if request.method == "POST":
        form = ApplicantProfileFormC(
            request.POST, request.FILES, instance=request.user.profile
        )
        if form.is_valid():
            data = form.cleaned_data["user"] = request.user
            section = data.profile.section
            if section == "C":
                data.profile.section = "D"
                data.profile.save()
            form.save()
            subject = "Interview Message"
            return redirect("application:ratewid", pk="Database")

    return render(
        request,
        "application/interview_process/firstinterview/sectionC.html",
        {"title": "First Section", "form": form},
    )


def first_interview(request):
    request.session["siteurl"] = settings.SITEURL
    section = UserProfile.objects.values_list("section", flat=True).get(
        user=request.user
    )

    context = {
        "alteryx_list": alteryx_list,
        "dba_list": dba_list,
        "tableau_list": tableau_list,
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
    UserProfile.objects.filter(applicant=request.user).update(section=section)
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

def policies(request):
    reporting_date = date.today() + timedelta(days=7)
    policies =Policy.objects.filter(Q(is_active=True),Q(is_internal=False)).order_by("upload_date")
    context = {"policies": policies, "reporting_date": reporting_date}
    return render(request, "application/orientation/policies.html", context)

# -------------------------rating Section-------------------------------------#

def rate(request):
    if request.method == "POST":
        form = RatingForm(request.POST, request.FILES, request=request)
        if request.user.is_staff or request.user.is_applicant:
            form.instance.employeename = request.user
        
        if form.is_valid():
            total_points=rewardpoints(form)
            form.instance.topic = "Other"
            form.instance.totalpoints = total_points
            
            # Saving form data to rating table only if the user is applicant
            if form.instance.employeename.is_applicant:
                upload_link_url = form.cleaned_data.get('uploadlinkurl')
                if not upload_link_url:
                    return render(request, "application/orientation/rate.html", {"form": form, "applicant_error": "Please provide the evidence link"})
                form.save()
                user_profile = UserProfile.objects.get(user__username=form.instance.employeename)
                if user_profile.section == "D":
                    return redirect("application:policies")
                else:
                    return redirect("application:section_"+user_profile.section.lower()+"")

            # For One on one sessions adding task points and increasing mxpoint if it is equal or near to points.
            try:
                task = Task.objects.filter(
                    Q(activity_name__icontains="one on one")
                ).get(employee__username=form.instance.employeename)
                task.point += total_points
                if task.point >= task.mxpoint or task.point + 15 >= task.mxpoint:
                    task.mxpoint += 15
                task.save()
                return redirect("management:new_evidence", taskid=task.id)
            except Task.DoesNotExist:
                print("Task does not exist")
        
    else:
        form = RatingForm(request=request)
    return render(request, "application/orientation/rate.html", {"form": form})




def ratewid(request,pk):
    if request.method == "POST":
        form = RatingForm(request.POST, request.FILES)
        if request.user.is_staff or request.user.is_applicant:
            print("employee or applicant",request.user)
            form.instance.employeename = request.user

        print(form.is_valid())
        if form.is_valid():
            totalpoints = 0
            try:
                if request.POST["projectDescription"] == "on":
                    totalpoints += 2
            except:
                pass
            try:
                if request.POST["requirementsAnalysis"] == "on":
                    totalpoints += 3
            except:
                pass
            try:
                if request.POST["development"] == "on":
                    totalpoints += 5
            except:
                pass
            try:
                if request.POST["testing"] == "on":
                    totalpoints += 3
            except:
                pass
            try:
                if request.POST["deployment"] == "on":
                    totalpoints += 2
            except:
                pass

            form.instance.topic = pk
            form.instance.totalpoints = totalpoints
            # Saving form data to rating table only if the user is applicant
            if form.instance.employeename.is_applicant == True:
                form.save()
                userprof = UserProfile.objects.get(user__username=form.instance.employeename)
                if userprof.section == "D":
                    return redirect("application:policies")
                else:   
                    return redirect("application:section_"+userprof.section.lower()+"")

            # For One on one sessions adding task points and increasing mxpoint if it is equal or near to points.
            try:
                idval,point, mxpoint = Task.objects.values_list("id","point", "mxpoint").filter(
                    Q(activity_name="one on one sessions")
                    | Q(activity_name="One on one sessions")
                    | Q(activity_name="One On One Sessions")
                    | Q(activity_name="One On One")
                    | Q(activity_name="one on one"),
                    employee__username=form.instance.employeename,
                )[0]
                point = point + totalpoints
                if point >= mxpoint or point + 15 >= mxpoint:
                    mxpoint += 15
                
                Task.objects.filter(
                    Q(activity_name="one on one sessions")
                    | Q(activity_name="One on one sessions")
                    | Q(activity_name="One On One Sessions")
                    | Q(activity_name="One On One")
                    | Q(activity_name="one on one"),
                    employee__username=form.instance.employeename,
                ).update(point=point, mxpoint=mxpoint)
                        
                return redirect(
                            "management:new_evidence", taskid=idval
                        )
            except:
                form = RatingForm()
                return render(request, "application/orientation/rate.html", {"form": form,"error":True})
    else:
        form = RatingForm()
    return render(request, "application/orientation/rate.html", {"form": form})


def enter_score(request):
    if request.method == "POST":
        form = RatingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("application:userscores", request.user )
    else:
        form = RatingForm()
    return render(request, "main/snippets_templates/generalform.html", {"form": form})

def rating(request):
    ratings = Rated.objects.all().order_by("-rating_date")

    context = {
        "ratings": ratings,
    }
    return render(request, "application/orientation/rating.html", context)


@login_required
def userscores(request, user=None, *args, **kwargs):
    request.session["siteurl"] = settings.SITEURL
    # employee=request.user
    employee = get_object_or_404(User, username=kwargs.get("username"))
    user_ratings=Rated.objects.filter(employeename=employee)
    # print(user_ratings)
    context = {
        'user_ratings': user_ratings,
        "title": "Student Scores",
    }
    # setting  up session
    request.session["employee_name"] = kwargs.get("username")
    return render(request, "application/orientation/intermediary_training.html", context)


class ScoresUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Rated
    template_name = 'main/snippets_templates/generalform.html'
    form_class = RatingForm  # Assuming you have a RatingForm in forms.py

    # verify the user's permissions.
    def test_func(self):
        # Assuming every logged in user can update the score. 
        # Change this condition as per your requirement.
        return self.request.user.is_authenticated

    def get_success_url(self):
        # Adjust the reverse URL as per your URL configuration
        return reverse("application:userscores", args=[str(self.request.user)])

    def form_valid(self, form):
        # Any logic you want to apply when the form is valid
        # Example: Set some fields, log something, etc.
        return super().form_valid(form)



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
    context={
        "trainees": trainees,
    }
    return render(request, "application/orientation/trainees.html",context)

class TraineeUpdateView(LoginRequiredMixin, UpdateView):
    model = Reporting
    fields = [
            "reporter",
            "rate",
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