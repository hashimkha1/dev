import itertools
from typing import List
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.urls import path, reverse
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
from main.utils import data_interview

from data.models import (
    Interviews,
    FeaturedCategory,
    FeaturedSubCategory,
    FeaturedActivity,
    ActivityLinks,
    DSU,
    Job_Tracker,
    JobRole,
    Interview_Questions,
    Prep_Questions

)
from data.filters import InterviewFilter, BitrainingFilter,QuestionFilter

# User=settings.AUTH_USER_MODEL
from data.forms import InterviewQuestionsForm
import json
from coda_project import settings

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
    context={
        "data_interview":data_interview
    }
    return render(request, "data/interview/interview_progress/start_interview.html",context)


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

@login_required
def prepquestions(request):
    questions = Prep_Questions.objects.all().order_by("-date")
    myFilter = QuestionFilter(request.GET, queryset=questions)
    questions = myFilter.qs
    context = {"questions": questions, "myFilter": myFilter}
    return render(request, "data/interview/prepquestions.html", context)

class PrepQuestionsCreateView(LoginRequiredMixin, CreateView):
	model = Prep_Questions
	success_url = "/data/prepquestions/"
	fields = ["company", 'category',"question", "response"]
	# fields = "__all__"

	def form_valid(self, form):
		# form.instance.user = self.request.user
		return super().form_valid(form)

class PrepQuestionsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Prep_Questions
    success_url = "/data/prepquestions/"
    fields = ["company", 'category',"question", "response"]
    # form = Prep_QuestionsForm()

    def form_valid(self, form):
        # form.instance.username = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user or self.request.user.is_admin or self.request.user.is_superuser:
            return True
        return False

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
         return render(request, "data/training/training_progress/courseoverview.html", context)

class TrainingView(LoginRequiredMixin, ListView):
    model = Interviews
    template_name = "data/training/training_progress/train.html"
    success_url = "/data/course"

    def get_context_data(self, **kwargs):
        try:
            context = super(TrainingView, self).get_context_data(**kwargs)
            context['title'] = FeaturedCategory.objects.all().first().title
            return context
        except:
            return redirect('data:jobroles')
            # return render(self.request, "data/training/training_progress/train.html")

class CourseView(LoginRequiredMixin, ListView):
    model = Interviews
    template_name = "data/training/training_progress/course.html"
    # success_url = "/data/course"





# ==================================INTERVIEW VIEWS====================================
class RoleListView(LoginRequiredMixin, ListView):
    queryset = JobRole.objects.all()
    template_name = "data/interview/interview_progress/interview_progress.html"
    success_url = "/data/project_story"


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

@method_decorator(login_required, name="dispatch")
class InterviewQuestionListView(ListView):
    queryset =Interview_Questions.objects.all()
    template_name = "data/interview/interviewquestion_upload.html"
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
    if request.method == 'GET':
        instance = JobRole.objects.get_by_question(question_type)
        form= InterviewForm()
        # questiontopic=['resume','methodology','testing']
        # value=request.path.split("/")
        # pathvalues = [i for i in value if i.strip()]
        # path=pathvalues[-1]
        # print(path)
        # url=f'data/interview/interview_progress/{question_type}s.html'
        url=f'data/interview/interview_progress/questions.html'
        # url="data/interview/interview_progress/" + str(instance) + ".html"
        print(url)
        context = {
            "form":form,
            "object": instance,
            "interviews": Interviews.objects.all(),
            # "path":path
        }
        if instance is None:
            return render(request, "main/errors/404.html")
        return render(request, url, context)
    if request.method == 'POST':
        try:
            form = InterviewForm(request.POST, request.FILES)
            if form.is_valid():
                form_data = form.cleaned_data
                data = Interviews.objects.filter(client=request.user, category=form_data['category'], question_type=question_type, link=form_data['link'], comment=form_data['comment'] )
                if data.exists():
                    messages.error(request, "you have already asked this question before")
                    return redirect('data:question-detail', question_type=question_type)
                instance = form.save(commit=False)
                instance.client = request.user
                instance.question_type = question_type
                instance.save()
                # data = form.cleaned_data
        except Exception as e:
            print(e)
            value=request.path
            message=value
            context={
                "message":message
            }
            print(message)
            return render(request, "main/errors/404.html",{"message":message})
        next_topic = JobRole.objects.filter(id__gt=JobRole.objects.get_by_question(question_type).id).order_by('id')
        if not next_topic.exists():
            return redirect('data:question-detail', question_type=question_type)
        return redirect('data:question-detail', question_type=next_topic.first().question_type)


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
    fields ="__all__"
    # fields =['category','question_type','doc','doclink','doclink',"desc1","desc2"]

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
    url=f'data/training/training_progress/training.html'
    context = {
        "form":form,
        "object": instance,
        # "categories": FeaturedCategory.objects.all()

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
    if request.method == "GET":
        instance = FeaturedSubCategory.objects.get_by_subcategory(title)
        # next_title = FeaturedSubCategory.objects.filter(id__gt=instance.id).order_by('id').first()
        form= InterviewQuestionsForm
        url=f'data/training/training_progress/course.html'
        context = {
            "form":form,
            "object": instance,
            "title_":title
            # "categories": FeaturedSubCategory.objects.all(),
        }
        if instance is None:
            return render(request, "main/errors/404.html")
        return render(request, url, context)

    if request.method == 'POST':
        try:
            form=InterviewQuestionsForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                # data = form.cleaned_data
        except Exception as e:
            print(e)
            return render(request, "main/errors/404.html")
        instance = FeaturedSubCategory.objects.get_by_subcategory(title)
        if instance is None:
            return render(request, "main/errors/404.html")
        next_title = FeaturedSubCategory.objects.filter(id__gt=instance.id).order_by('id')
        if not next_title.exists():
            next_category = FeaturedCategory.objects.filter(id__gt=instance.featuredcategory.id).order_by('id').first()
            return redirect('data:category-detail', title=next_category.title)
        next_title = next_title.first()
        return redirect('data:subcategory-detail', title=next_title.title)

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
    # fields = ["Activity", "link_name", "doc", "link", "is_active"]
    fields = ["Activity", "link_name", "doc", "link"]

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
    fields = ["Activity", "link_name", "doc", "link"]

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
    template_name = "data/training/updatelist.html"

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

class LinksListView(ListView):
    model= ActivityLinks
    template_name = "data/training/links.html"
    context_object_name='links'

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

def employetraining(request):
    request.session["siteurl"] = settings.SITEURL
    with open(settings.STATIC_ROOT + '/employeetraining.json', 'r') as file:
        data = json.load(file)

    return render(
        request, "data/training/employeetraining.html", {"title": "employeeetraining", "data":data}
    )

def updatelinks_employetraining(request):
    department = request.POST["department"]
    subdepartment = request.POST["subdepartment"]
    linkname = request.POST["linkname"]
    link_url = request.POST["link_url"]

    with open(settings.STATIC_ROOT + '/employeetraining.json', "r") as jsonFile:
        data = json.load(jsonFile)

    if subdepartment == "":
        data[department][linkname] = link_url
    else:
        data[department][subdepartment][linkname] = link_url

    with open(settings.STATIC_ROOT + '/employeetraining.json', "w") as jsonFile:
        json.dump(data, jsonFile)
    return JsonResponse({"success": True})