from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
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
from data.forms import InterviewForm, DSUForm  # , UploadForm

from data.models import (
    Interviews,
    FeaturedCategory,
    FeaturedSubCategory,
    FeaturedActivity,
    ActivityLinks,
    DSU,
    Job_Tracker,  # , DocUpload
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


# interview starts
@login_required
def interview(request):
    return render(request, "data/interview/interview.html")


@login_required
def resume(request):

    return render(request, "data/interview/interview_progress/resume.html")


@login_required
def project_story(request):
    return render(request, "data/interview/interview_progress/project_story.html")


@login_required
def introduction(request):
    return render(request, "data/interview/interview_progress/introduction.html")


@login_required
def agile_vs_waterfall(request):
    return render(request, "data/interview/interview_progress/agile_vs_waterfall.html")


@login_required
def performance_tuning(request):
    return render(request, "data/interview/interview_progress/performance_tuning.html")


@login_required
def sdlc(request):
    return render(request, "data/interview/interview_progress/sdlc.html")


@login_required
def testing(request):
    return render(request, "data/interview/interview_progress/testing.html")


@login_required
def environment(request):
    return render(request, "data/interview/interview_progress/environment.html")


# interview ends


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


# ==================================INTERVIEW VIEWS====================================
class InterviewCreateView(LoginRequiredMixin, CreateView):
    model = Interviews
    # success_url = "/data/iuploads"
    fields = ["category", "question_type", "doc", "link"]

    def get_success_url(self):
        data = Interviews.objects.filter(client=self.request.user)
        # print(data, "HERE  GOES THE DATA")
        question_types = []
        for i in data:
            question_types.append(i.question_type)
        print(question_types)
        if "Project Story" not in question_types:
            return reverse("data:project_story")
        elif "introduction" not in question_types:
            return reverse("data:introduction")
        elif "methodology" not in question_types:
            return reverse("data:agile_vs_waterfall")
        elif "performance" not in question_types:
            return reverse("data:performance_tuning")
        elif "sdlc" not in question_types:
            return reverse("data:sdlc")
        elif "testing" not in question_types:
            return reverse("data:testing")
        elif "environment" not in question_types:
            return reverse("data:environment")
        else:
            return reverse("data:interview")

    def form_valid(self, form):
        form.instance.client = self.request.user
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
# ========================1. CREATION OF VIEWS============================


@method_decorator(login_required, name="dispatch")
class FeaturedCategoryCreateView(LoginRequiredMixin, CreateView):
    model = FeaturedCategory
    success_url = "/data/bitraining2"
    fields = ["title", "description"]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class FeaturedSubCategoryCreateView(LoginRequiredMixin, CreateView):
    model = FeaturedSubCategory
    success_url = "/data/bitraining2"
    fields = ["featuredcategory", "title", "description"]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class FeaturedActivityCreateView(LoginRequiredMixin, CreateView):
    model = FeaturedActivity
    success_url = "/data/bitraining2"
    fields = ["featuredsubcategory", "activity_name", "description"]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


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
