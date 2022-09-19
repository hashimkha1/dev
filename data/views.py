import itertools
from typing import List
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    DetailView,
    UpdateView,
)
from data.forms import InterviewForm, DSUForm ,RoleForm

from data.models import (
    Interviews,
    FeaturedCategory,
    FeaturedSubCategory,
    FeaturedActivity,
    ActivityLinks,
    DSU,
    Job_Tracker,
    JobRole
)
from data.filters import InterviewFilter, BitrainingFilter  # ,UserFilter

# User=settings.AUTH_USER_MODEL
User = get_user_model()


def analysis(request):
    return render(
        request, "main/home_templates/analysis_home.html", {"title": "analysis"}
    )


def deliverable(request):
    return render(
        request, "data/deliverable/deliverable.html", {"title": "deliverable"}
    )


@login_required
def training(request):
    return render(request, "data/training/training.html", {"title": "training"})


@login_required
def training_v2(request):
    return render(request, "data/training/training_v2.html", {"title": "training_v2"})


@login_required
def bitraining(request):
    return render(request, "data/training/bitraining.html", {"title": "training"})


@login_required
def bi_training(request):
    return render(request, "data/training/bi_training.html", {"title": "training"})


# interview starts
@login_required
def interview(request):
    return render(request, "data/interview/interview.html")


def payroll(request):
    return render(request, "data/deliverable/payroll.html", {"title": "payroll"})


def financialsystem(request):
    return render(
        request, "data/deliverable/financialsystem.html", {"title": "financialsystem"}
    )


def project(request):
    return render(request, "data/deliverable/project.html", {"title": "project"})


# views on samples reports.
def report(request):
    return render(request, "data/documents/report.html", {"title": "report"})


def database(request):
    return render(request, "data/database.html", {"title": "report"})


def etl(request):
    return render(request, "data/etl.html", {"title": "etl"})


def getdata(request):
    return render(request, "data/getdata.html", {"title": "getdata"})


def pay(request):
    return render(request, "data/pay.html", {"title": "pay"})


# Views on interview Section


@login_required
def uploadinterview(request):

    if request.method == "POST":
        data = Interviews.objects.all()
        print(data, "HERE  GOES THE DATA")
        form = InterviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("data:interviewlist")
    else:
        form = InterviewForm()
    return render(request, "data/interview/uploadinterview.html", {"form": form})


@login_required
def dsu_entry(request):
    if request.method == "POST":
        form = DSUForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("data:dsu")
    else:
        form = DSUForm()
    return render(request, "data/training/form_templates/dsu_form.html", {"form": form})


# for uploading interviews


@login_required
def iuploads(request):
    uploads = Interviews.objects.all().order_by("-upload_date")
    myFilter = InterviewFilter(request.GET, queryset=uploads)
    uploads = myFilter.qs
    context = {"uploads": uploads, "myFilter": myFilter}
    return render(request, "data/interview/interviewuploads.html", context)


def useruploads(request, pk=None, *args, **kwargs):
    useruploads = Interviews.objects.filter(user=request.user).order_by("-upload_date")
    context = {
        "useruploads": useruploads,
    }
    return render(request, "data/interview/useruploads.html", context)


# ==================================TRAINING VIEWS====================================

# class CourseView(LoginRequiredMixin, CreateView):
#     model = Interviews
#     form_class = InterviewForm
#     template_name = "data/training/training_progress/main.html"
#     success_url = "/data/project_story"
#     # fields = ["category", "doc", "link", "answer_to_question"]

#     def form_valid(self, form):
#         form.instance.client = self.request.user
#         form.instance.question_type = "project story"
#         print("form.instance.question_type")
#         return super().form_valid(form)

def courseoverivew(request): #, question_type=None, *args, **kwargs):
    instance = request.path
    value=request.path.split("/")
    instance = [i for i in value if i.strip()]
    context={
        "instance":instance
    }
    if instance is None:
        return render(request, "main/errors/404.html")
    else:
         return render(request, "data/training/training_progress/courseoverview.html", context )

class TrainingView(LoginRequiredMixin, ListView):
    model = Interviews
    template_name = "data/training/training_progress/train.html"
    success_url = "/data/course"

class CourseView(LoginRequiredMixin, ListView):
    model = Interviews
    template_name = "data/training/training_progress/course.html"
    # success_url = "/data/course"





# ==================================INTERVIEW VIEWS====================================
class RoleListView(LoginRequiredMixin, ListView):
    queryset = JobRole.objects.all()
    template_name = "data/interview/interview_progress/interview_progress.html"
    success_url = "/data/project_story"


class ResumeView(LoginRequiredMixin, CreateView):
    queryset = JobRole.objects.all()
    model = Interviews
    form_class = InterviewForm
    template_name = "data/interview/interview_progress/resume.html"
    success_url = "/data/project_story"
    interviews = Interviews.objects.all()
    form= InterviewForm

    def form_valid(self, form):
        form.instance.client = self.request.user
        form.instance.question_type = "project story"
        print("form.instance.question_type")
        return super().form_valid(form)


class ProjectStoryView(LoginRequiredMixin, CreateView):
    model = Interviews
    form_class = InterviewForm
    template_name = "data/interview/interview_progress/project_story.html"
    success_url = "/data/introduction"
    # fields = ["category", "doc", "link", "answer_to_question"]

    def form_valid(self, form):
        form.instance.client = self.request.user
        form.instance.question_type = "project story"
        print("form.instance.question_type")
        return super().form_valid(form)


class IntroductionView(LoginRequiredMixin, CreateView):
    model = Interviews
    form_class = InterviewForm
    template_name = "data/interview/interview_progress/introduction.html"
    success_url = "/data/sdlc"
    # fields = ["category", "doc", "link", "answer_to_question"]

    def form_valid(self, form):
        form.instance.client = self.request.user
        form.instance.question_type = "introduction"
        return super().form_valid(form)


class SDLCView(LoginRequiredMixin, CreateView):
    model = Interviews
    form_class = InterviewForm
    template_name = "data/interview/interview_progress/sdlc.html"
    success_url = "/data/methodology"
    # fields = ["category", "doc", "link", "answer_to_question"]

    def form_valid(self, form):
        form.instance.client = self.request.user
        form.instance.question_type = "sdlc"
        return super().form_valid(form)


class MethodologyView(LoginRequiredMixin, CreateView):
    model = Interviews
    form_class = InterviewForm
    template_name = "data/interview/interview_progress/methodology.html"
    success_url = "/data/performance_tuning"
    # fields = ["category", "doc", "link", "answer_to_question"]

    def form_valid(self, form):
        form.instance.client = self.request.user
        form.instance.question_type = "methodology"
        return super().form_valid(form)


class PerformanceView(LoginRequiredMixin, CreateView):
    model = Interviews
    form_class = InterviewForm
    template_name = "data/interview/interview_progress/performance_tuning.html"
    success_url = "/data/environment"
    # fields = ["category", "doc", "link", "answer_to_question"]

    def form_valid(self, form):
        form.instance.client = self.request.user
        form.instance.question_type = "performance"
        return super().form_valid(form)


class EnvironmentView(LoginRequiredMixin, CreateView):
    model = Interviews
    form_class = InterviewForm
    template_name = "data/interview/interview_progress/environment.html"
    success_url = "/data/testing"
    # fields = ["category", "doc", "link", "answer_to_question"]

    def form_valid(self, form):
        form.instance.client = self.request.user
        form.instance.question_type = "environment"
        return super().form_valid(form)


class TestingView(LoginRequiredMixin, CreateView):
    model = Interviews
    form_class = InterviewForm
    template_name = "data/interview/interview_progress/testing.html"
    success_url = "/data/interview"
    # fields = ["category", "doc", "link", "answer_to_question"]

    def form_valid(self, form):
        form.instance.client = self.request.user
        form.instance.question_type = "testing"
        return super().form_valid(form)

class InterviewCreateView(LoginRequiredMixin, CreateView):
    model = Interviews
    form_class = InterviewForm
    template_name = "data/interview/interview_form.html"
    success_url = "/data/iuploads/"

    def form_valid(self, form):
        form.instance.client = self.request.user
        # form.instance.question_type = "testing"
        return super().form_valid(form)


class InterviewCreateView(LoginRequiredMixin, CreateView):
    model = Interviews
    form_class = InterviewForm
    template_name = "data/interview/interview_form.html"
    success_url = "/data/iuploads/"

    def form_valid(self, form):
        form.instance.client = self.request.user
        # form.instance.question_type = "testing"
        return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
class InterviewListView(ListView):
    queryset = Interviews.objects.all()
    template_name = "data/interview/iuploads.html"
    ordering = ["-upload_date"]


class ClientInterviewListView(ListView):
    model = Interviews
    context_object_name = "client_interviews"
    template_name = "data/interview/user_interviews.html"

    # paginate_by = 5
    def get_queryset(self):
        # request=self.request
        # user=self.kwargs.get('user')
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        # tasks=Task.objects.all().filter(client=client)
        return Interviews.objects.all().filter(user=user)


@method_decorator(login_required, name="dispatch")
class InterviewDetailView(DetailView):
    model = Interviews
    ordering = ["-upload_date"]

# @method_decorator(login_required, name="dispatch")
# class QuestionDetailView(DetailView):
#     model = Interviews
#     ordering = ["-upload_date"]


def courseview(request, question_type=None, *args, **kwargs):
    instance = JobRole.objects.get_by_question(question_type)
    form= InterviewForm
    questiontopic=['resume','methodology','testing']
    value=request.path.split("/")
    pathvalues = [i for i in value if i.strip()]
    path=pathvalues[-1]
    print(path)
    # url=f'data/interview/interview_progress/{question_type}s.html'
    url=f'data/interview/interview_progress/questions.html'
    # url="data/interview/interview_progress/" + str(instance) + ".html"
    print(url)
    context = {
        "form":form,
        "object": instance,
        "interviews": Interviews.objects.all(),
        "path":path
    }
    if instance is None:
        return render(request, "main/errors/404.html")
    return render(request, url, context)


def questionview(request, question_type=None, *args, **kwargs):
    instance = JobRole.objects.get_by_question(question_type)
    form= InterviewForm
    questiontopic=['resume','methodology','testing']
    value=request.path.split("/")
    pathvalues = [i for i in value if i.strip()]
    path=pathvalues[-1]
    print(path)
    # url=f'data/interview/interview_progress/{question_type}s.html'
    url=f'data/interview/interview_progress/questions.html'
    # url="data/interview/interview_progress/" + str(instance) + ".html"
    print(url)
    context = {
        "form":form,
        "object": instance,
        "interviews": Interviews.objects.all(),
        "path":path
    }
    if instance is None:
        return render(request, "main/errors/404.html")
    return render(request, url, context)


@method_decorator(login_required, name="dispatch")
class InterviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Interviews
    success_url = "/data/iuploads"
    fields = [
        "client",
        "category",
        "question_type",
        "doc",
        "link",
    ]

    def form_valid(self, form):
        # form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        interview = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user == interview.client:
            return True
        return False


@method_decorator(login_required, name="dispatch")
class InterviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Interviews
    success_url = "/data/iuploads"

    def test_func(self):
        # timer = self.get_object()
        # if self.request.user == timer.author:
        # if self.request.user.is_superuser:
        if self.request.user.is_superuser:
            return True
        return False


# ==================================TRAINING VIEWS====================================
@method_decorator(login_required, name="dispatch")
class RoleCreateView(LoginRequiredMixin, CreateView):
    model = JobRole
    form_class = RoleForm
    template_name = "data/jobroles/role.html"
    success_url = "/data/roles/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
class RolesView(LoginRequiredMixin, ListView):
    queryset  = JobRole.objects.all()
    template_name = "data/jobroles/roles.html"

@method_decorator(login_required, name="dispatch")
class RoleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JobRole
    template_name = "data/jobroles/role.html"
    success_url = "/data/roles"
    fields =['category','question_type','doc','doclink','doclink',"desc1","desc2"]

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

    def test_func(self):
        editor=self.request.user
        JobRole = self.get_object()
        if editor.is_superuser or  editor.is_admin :
            return True
        elif editor == JobRole.user:
            return True
        return redirect("data:jobroles")


@method_decorator(login_required, name="dispatch")
class RoleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = JobRole
    template_name = "data/jobroles/jobrole_confirm_delete.html"
    success_url = "/data/roles"

    def test_func(self):
        editor=self.request.user
        JobRole = self.get_object()
        if editor.is_superuser or  editor.is_admin :
            return True
        elif editor == JobRole.user:
            return True
        return False

# ========================1. CREATION OF VIEWS============================


@method_decorator(login_required, name="dispatch")
class FeaturedCategoryCreateView(LoginRequiredMixin, CreateView):
    model = FeaturedCategory
    success_url = "/data/bitraining2"
    fields = ["title", "description"]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

def categorydetail(request, title=None, *args, **kwargs):
    instance = FeaturedCategory.objects.get_by_category(title)
    form= InterviewForm
    print(instance)
    # url=f'data/training/training_progress/{title}s.html'
    url=f'data/training/training_progress/training.html'
    # url="data/training/training_progress/" + str(instance) + ".html"
    print(url)
    context = {
        "form":form,
        "object": instance,
        "categories": FeaturedCategory.objects.all()

    }
    if instance is None:
        return render(request, "main/errors/404.html")
    return render(request, url, context)


@method_decorator(login_required, name="dispatch")
class FeaturedSubCategoryCreateView(LoginRequiredMixin, CreateView):
    model = FeaturedSubCategory
    success_url = "/data/bitraining2"
    fields = ["featuredcategory", "title", "description"]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

def subcategorydetail(request, title=None, *args, **kwargs):
    instance = FeaturedSubCategory.objects.get_by_subcategory(title)
    form= InterviewForm
    print(instance)
    url=f'data/training/training_progress/course.html'
    print(url)
    context = {
        "form":form,
        "object": instance,
        # "categories": FeaturedSubCategory.objects.all(),
    }
    if instance is None:
        return render(request, "main/errors/404.html")
    return render(request, url, context)

@method_decorator(login_required, name="dispatch")
class FeaturedActivityCreateView(LoginRequiredMixin, CreateView):
    model = FeaturedActivity
    success_url = "/data/bitraining2"
    fields = ["featuredsubcategory", "activity_name", "description"]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

def activitydetail(request, slug=None, *args, **kwargs):
    # instance = FeaturedActivity.objects.get_by_slug(slug)
    activities = FeaturedActivity.objects.all()
    print(activities)
    url=f'data/training/training_progress/activity.html'
    print(url)
    context = {
        "form":InterviewForm,
        "activities": activities,
        "categories": FeaturedSubCategory.objects.all(),
    }
    if activities is None:
        return render(request, "main/errors/404.html")
    return render(request, url, context)


@method_decorator(login_required, name="dispatch")
class FeaturedActivityLinksCreateView(LoginRequiredMixin, CreateView):
    model = ActivityLinks
    success_url = "/data/bitraining2"
    fields = ["Activity", "link_name", "doc", "link", "is_active"]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class DSUCreateView(LoginRequiredMixin, CreateView):
    model = DSU
    success_url = "/data/bitraining"
    fields = ["trained_by", "category", "task", "plan", "challenge", "is_active"]

    def form_valid(self, form):
        form.instance.trained_by = self.request.user
        return super().form_valid(form)


# ========================2. UPDATE VIEWS============================
@method_decorator(login_required, name="dispatch")
class FeaturedCategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FeaturedCategory
    success_url = "/data/updatelist"
    # fields=['group','category','employee','activity_name','description','point','mxpoint','mxearning']
    fields = ["title", "description"]

    def form_valid(self, form):
        # form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        FeaturedCategory = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user == FeaturedCategory.created_by:
            return True
        return redirect("data:activity-list")


@method_decorator(login_required, name="dispatch")
class FeaturedSubCategoryUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = FeaturedSubCategory
    success_url = "/data/updatelist"
    # fields=['group','category','employee','activity_name','description','point','mxpoint','mxearning']
    fields = ["featuredcategory", "title", "description"]

    def form_valid(self, form):
        # form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        FeaturedSubCategory = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user == FeaturedSubCategory.created_by:
            return True
        return redirect("data:activity-list")


@method_decorator(login_required, name="dispatch")
class FeaturedActivityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FeaturedActivity
    success_url = "/data/updatelist"
    # fields=['group','category','employee','activity_name','description','point','mxpoint','mxearning']
    fields = ["featuredsubcategory", "activity_name", "description"]

    def form_valid(self, form):
        # form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        FeaturedActivity = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user == FeaturedActivity.created_by:
            return True
        return redirect("data:activity-list")


@method_decorator(login_required, name="dispatch")
class FeaturedActivityLinksUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = ActivityLinks
    success_url = "/data/updatelist"
    # fields=['group','category','employee','activity_name','description','point','mxpoint','mxearning']
    fields = ["activity", "link_name", "doc", "link"]

    def form_valid(self, form):
        # form.instance.author=self.request.user
        return super().form_valid(form)

    def test_func(self):
        ActivityLinks = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user == ActivityLinks.created_by:
            return True
        return redirect("data:activity-list")


# ========================3. DELETE VIEWS============================
@method_decorator(login_required, name="dispatch")
class FeaturedCategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FeaturedCategory
    success_url = "/data/updatelist"

    def test_func(self):
        # timer = self.get_object()
        # if self.request.user == timer.author:
        # if self.request.user.is_superuser:
        if self.request.user.is_superuser:
            return True
        return False


@method_decorator(login_required, name="dispatch")
class FeaturedSubCategoryDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    model = FeaturedCategory
    success_url = "/data/updatelist"

    def test_func(self):
        # timer = self.get_object()
        # if self.request.user == timer.author:
        # if self.request.user.is_superuser:
        if self.request.user.is_superuser:
            return True
        return False


@method_decorator(login_required, name="dispatch")
class FeaturedActivityDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FeaturedActivity
    success_url = "/data/updatelist"

    def test_func(self):
        # timer = self.get_object()
        # if self.request.user == timer.author:
        # if self.request.user.is_superuser:
        if self.request.user.is_superuser:
            return True
        return False


@method_decorator(login_required, name="dispatch")
class FeaturedActivityLinksDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    model = ActivityLinks
    success_url = "/data/updatelist"

    def test_func(self):
        # timer = self.get_object()
        # if self.request.user == timer.author:
        # if self.request.user.is_superuser:
        if self.request.user.is_superuser:
            return True
        return False


# ========================4. DISPLAY/LIST VIEWS============================
class FeaturedCategoryListView(ListView):
    queryset = FeaturedCategory.objects.all()
    template_name = "management/daf/updatelist.html"


def activity_view(request):
    categories = (
        FeaturedCategory.objects.prefetch_related("featuredsubcategory_set").all(),
    )
    cats = FeaturedCategory.objects.all().order_by("-created_at")
    BiFilter = BitrainingFilter(request.GET, queryset=cats)
    categories = BiFilter.qs

    context = {"categories": categories, "cats": cats, "BiFilter": BiFilter}
    return render(
        request=request, template_name="data/training/bitraining2.html", context=context
    )


def table_activity_view(request):
    categories = (
        FeaturedCategory.objects.prefetch_related("featuredsubcategory_set").all(),
    )
    cats = FeaturedCategory.objects.all()  # .order_by('-created_at')
    BiFilter = BitrainingFilter(request.GET, queryset=cats)
    categories = BiFilter.qs

    context = {"categories": categories, "cats": cats, "BiFilter": BiFilter}
    return render(
        request=request, template_name="data/training/updatelist.html", context=context
    )


class DSUListView(ListView):
    queryset = DSU.objects.all().order_by("-created_at")
    template_name = "data/training/dsu.html"


# =============================Job===================
@method_decorator(login_required, name="dispatch")
class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job_Tracker
    success_url = "/data/job_tracker"
    fields = [
        "position",
        "recruiter",
        "vendor_phone",
        "primary_tool",
        "secondary_tool",
        "job_location",
        "offer",
        "description",
        "status",
        "updated_resume",
    ]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class JobListView(ListView):
    queryset = Job_Tracker.objects.all()
    template_name = "data/interview/job_tracker.html"
    ordering = ["-created_at"]


def userjobtracker(request, user=None, *args, **kwargs):
    user = get_object_or_404(User, username=kwargs.get("username"))
    jobs = Job_Tracker.objects.all().filter(created_by=user).order_by("-created_at")
    num = jobs.count()
    # my_time=jobs.aggregate(Assigned_Time=Avg('time'))
    # Used=jobs.aggregate(Used_Time=Sum('duration'))
    # Usedtime=Used.get('Used_Time')
    Usedtime = 1
    # plantime=my_time.get('Assigned_Time')
    plantime = 1
    try:
        delta = round(plantime - Usedtime)
    except (TypeError, AttributeError):
        delta = 0
        return render(request, "testing/job_tracker.html")
    context = {
        "jobs": jobs,
        "num": num,
        "plantime": plantime,
        "Usedtime": Usedtime,
        "delta": delta,
    }

    return render(request, "data/interview/userjobtracker.html", context)
