from django.db.models import Q
from django.utils.text import capfirst
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from main.models import Service,ServiceCategory, Pricing
from django.views.generic import (
        CreateView,
        DeleteView,
        ListView,
        DetailView,
        UpdateView,
    )
from data.forms import (
    PrepQuestionsForm,TrainingResponseForm,
    InterviewForm, DSUForm ,RoleForm,
)
from main.utils import data_interview,Meetings,path_values,job_support,split_sentences
from main.context_processors import image_view
from data.models import (
    Interviews,
    FeaturedCategory,
    FeaturedSubCategory,
    FeaturedActivity,
    ActivityLinks,
    DSU,
    Job_Tracker,
    JobRole,
    Training_Responses,
    Prep_Questions,
    TrainingResponsesTracking
)
from data.filters import InterviewFilter, BitrainingFilter,QuestionFilter,ResponseFilter

# User=settings.AUTH_USER_MODEL
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



# @login_required
# def training_v2(request):
#     print("I am with Sylivia")
#     return render(request, "data/training/training_v2.html", {"title": "training_v2"})
    

@login_required
def start_training(request, slug=None, *args, **kwargs):
    path_list, sub_title, pre_sub_title = path_values(request)
    try:
        service_shown = Service.objects.get(slug="data_analysis")
    except Service.DoesNotExist:
        return redirect('main:layout')
    service_categories = ServiceCategory.objects.filter(service=service_shown.id)
    category_slug=None
    category_name=None
    category_id=None
    for item in service_categories:
        if item.slug==slug:
            category_slug=item.slug
            category_name=item.name
            description=item.description
            data_items=data_interview,

    onboarding_description,troubleshooting_description,requirement_description=split_sentences(description)

    if category_slug == 'interview':
        data_items=data_interview
    else:
        data_items=job_support

    context = {}
    context = {
        "SITEURL": settings.SITEURL,
        "data_items":data_items,
        "title": category_name,
        "category_slug": category_slug,
        "description": description,
        "onboarding_description": onboarding_description,
        "requirement_description": requirement_description,
        "troubleshooting_description": troubleshooting_description
    }
    return render(request, "data/interview/interview_progress/start_interview.html",context)


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
    useruploads = Interviews.objects.filter(client=request.user).order_by("-upload_date")
    context = {
        "useruploads": useruploads,
    }
    return render(request, "data/interview/useruploads.html", context)
    
@login_required
def prepquestions(request):
    questions= Prep_Questions.objects.filter(Q(is_answered=None) | Q(is_answered=False)).order_by("date")
    QuestionsFilter = QuestionFilter(request.GET, queryset=questions)
    questions = QuestionFilter.qs
    context = {"questions": questions, "myFilter": QuestionsFilter}
    return render(request, "data/interview/interview_progress/prepquestions.html", context)

def prep_responses(request):
    companies=Prep_Questions.objects.values_list('company', flat=True).distinct()
    responses = Prep_Questions.objects.filter(Q(is_answered=True)).order_by("-updated_at")
    client_responses = Prep_Questions.objects.filter(Q(is_answered=True),Q(questioner=request.user)).order_by("-updated_at")
    ResFilter = ResponseFilter(request.GET, queryset=responses)

    context_a = {                
            "companies": companies, 
            "responses": responses, 
            "ResFilter": ResponseFilter(request.GET, queryset=responses),
    }
    context_b = {                
            "companies": companies, 
            "responses": client_responses,
            "ResFilter": ResponseFilter(request.GET, queryset=client_responses),
    }
    # return render(request, "data/interview/interview_progress/test.html", context)
    if request.user.is_superuser or request.user.is_staff:
        return render(request, "data/interview/interview_progress/prepresponses.html", context_a)
    if request.user.is_client:
        return render(request, "data/interview/interview_progress/prepresponses.html", context_b)
    else:
        context={
            "title":"ARE YOU A CLIENT/STUDENT?",
            "contact":f'Kindly,contact admin at info@codanalytics.net!',
            "message":f'Hi,{request.user}, you are currently not authorized to access this page.'
        }
        return render(request, "main/errors/generalerrors.html", context)
    
class PrepQuestionsCreateView(LoginRequiredMixin, CreateView):
    model = Prep_Questions
    success_url = "/data/prepquestions/"
    template_name="data/interview/interview_progress/prep_questions_form.html"
    form_class=PrepQuestionsForm

    def form_valid(self, form):
        form.instance.questioner = self.request.user
        return super().form_valid(form)
class PrepQuestionsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Prep_Questions
    success_url = "/data/prepquestions/"
    form_class=PrepQuestionsForm
    # fields = ["company", 'position','category',"question", "response","is_answered"]
    def form_valid(self, form):
        # form.instance.username = self.request.user
        return super().form_valid(form)
    def test_func(self):
        if self.request.user or self.request.user.is_admin or self.request.user.is_superuser:
            return True
        return False
# ==================================TRAINING VIEWS====================================
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
    template_name = "data/interview/interviewuploads.html"
    ordering = ["-upload_date"]

@method_decorator(login_required, name="dispatch")
class TrainingResponseListView(ListView):
    queryset =Training_Responses.objects.all()
    template_name = "data/interview/interviewquestion_upload.html"
    ordering = ["-upload_date"]

class ClientInterviewListView(ListView):
    model = Interviews
    context_object_name = "client_interviews"
    template_name = "data/interview/user_interviews.html"
    # paginate_by = 5
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        # tasks=Task.objects.all().filter(client=client)
        return Interviews.objects.all().filter(user=user)

@method_decorator(login_required, name="dispatch")
class InterviewDetailView(DetailView):
    model = Interviews
    ordering = ["-upload_date"]

def courseview(request, question_type=None, *args, **kwargs):
    instance = JobRole.objects.get_by_question(question_type)
    form= InterviewForm
    questiontopic=['resume','methodology','testing']
    value=request.path.split("/")
    pathvalues = [i for i in value if i.strip()]
    path=pathvalues[-1]
    print(path)
    url=f'data/interview/interview_progress/questions.html'
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
    question_mapping = {
        'performance': ['tableau', 'alteryx', 'sql', 'python'],
        'testing': ['project', 'test_types', 'process'],
        'introduction': ['domain_industry', 'role', 'system_security', 'project_management', 'data_tools', 'communication'],
        'sdlc': ['initiation', 'planning', 'design', 'development', 'testing', 'deployment', 'maintenance'],
        'Project Story': ['description', 'deliverables', 'challenges', 'solutions'],
        'resume': ['summary', 'skills', 'responsibilities'],
        'methodology': ['projects', 'releases', 'sprints', 'stories'],
    }
    if request.method == 'GET':
        # print('question_typ==============e',question_type)
        instance = JobRole.objects.get_by_question(question_type)
        form= InterviewForm()
        required_fields = question_mapping.get(question_type, [])
        for field_name in required_fields:
            form.fields[field_name].required = True
            
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
            required_fields = question_mapping.get(question_type, [])
            for field_name in required_fields:
                form.fields[field_name].required = True
            if form.is_valid():
                form_data = form.cleaned_data
                data = Interviews.objects.filter(client=request.user, category=form_data['category'], question_type=question_type, link=form_data['link'], comment=form_data['comment'] )
                if data.exists():
                    messages.error(request, "you have already asked this question before")
                    return redirect('data:question-detail', question_type=question_type)
                instance = form.save(commit=False)
                instance.client = request.user
                instance.question_type = question_type
                dynamic_fields = {field: form_data[field] for field in required_fields}
                # Convert the dynamic_fields dictionary to a JSON string
                dynamic_fields_json = json.dumps(dynamic_fields)
                # Save the JSON string to the instance's dynamic_fields field
                instance.dynamic_fields = dynamic_fields_json
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
    success_url = "/data/bitraining"
    fields = ["title", "description"]
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

def categorydetail(request, title=None, *args, **kwargs):
    instance = FeaturedCategory.objects.get_by_category(title)
    tasks=FeaturedActivity.objects.all()

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
    page_title = 'Add Sub Category'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title']=capfirst(self.page_title)

def subcategorydetail(request, title=None, *args, **kwargs):
    if request.user.category == 4:
        try:
            tracking = TrainingResponsesTracking.objects.get(user=request.user)
            if title != tracking.featuredsubcategory.title:
                return redirect('data:subcategory-detail', title=tracking.featuredsubcategory.title)
        except:
            tracking = TrainingResponsesTracking()
            obj = FeaturedSubCategory.objects.get(title=title)
            tracking.user = request.user
            tracking.featuredsubcategory = obj
            tracking.save()

        instance = FeaturedSubCategory.objects.get_by_subcategory(title)
        
        if request.method == 'POST':
            try:
                form=TrainingResponseForm(request.POST, request.FILES)
                if form.is_valid():
                    form_obj = form.save(commit=False)
                    form_obj.user = request.user
                    form_obj.save()
            except Exception as e:
                return render(request, "main/errors/404.html")

            if instance is None:
                return render(request, "main/errors/404.html")

            next_title = FeaturedSubCategory.objects.filter(order__gt=instance.order).order_by('order')
            print(next_title)
            if not next_title.exists():
                next_category = FeaturedCategory.objects.filter(title='Course Overview').first()
                tracking.featuredsubcategory = FeaturedSubCategory.objects.get(order='1')
                tracking.save()
                print(tracking.featuredsubcategory)
                return redirect('data:category-detail', title=next_category.title)
            next_title = next_title.first()
            tracking.featuredsubcategory = next_title
            tracking.save()
            return redirect('data:subcategory-detail', title=next_title.title)
    else:
        instance = FeaturedSubCategory.objects.get_by_subcategory(title)
    tasks= FeaturedActivity.objects.filter(featuredsubcategory=instance.id)
    url= f'data/training/training_progress/course.html'
    context = {
        "tasks": tasks,
        "form": TrainingResponseForm,
        "object": instance,
        "title_": title
    }
    if instance is None:
        return render(request, "main/errors/404.html")
    return render(request, url, context)


@method_decorator(login_required, name="dispatch")
class FeaturedActivityCreateView(LoginRequiredMixin, CreateView):
    model = FeaturedActivity
    success_url = "/data/bitraining"
    fields = ["featuredsubcategory", "activity_name", "description","guiding_question","interview_question"]
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

def activitydetail(request, slug=None, *args, **kwargs):
    # instance = FeaturedActivity.objects.get_by_slug(slug)
    activities = FeaturedActivity.objects.all()
    url=f'data/training/training_progress/activity.html'
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
        return redirect("data:training-list")
    
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
        return redirect("data:training-list")
    
@method_decorator(login_required, name="dispatch")
class FeaturedActivityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FeaturedActivity
    success_url = "/data/updatelist"
    # fields=['group','category','employee','activity_name','description','point','mxpoint','mxearning']
    fields = ["featuredsubcategory", "activity_name","guiding_question","interview_question", "description"]
    def form_valid(self, form):
        # form.instance.author=self.request.user
        return super().form_valid(form)
    def test_func(self):
        FeaturedActivity = self.get_object()
        if self.request.user.is_superuser:
            return True
        elif self.request.user == FeaturedActivity.created_by:
            return True
        return redirect("data:training-list")
    
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
        return redirect("data:training-list")
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
        request=request, template_name="data/training/bitraining.html", context=context
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

def feedback(request):
    value=request.path.split("/")
    instance = [i for i in value if i.strip()]
    title=instance[-1]
    queryset = DSU.objects.all().order_by("-created_at")
    responses = Training_Responses.objects.all().order_by("-upload_date")
    print(responses)
    context={
                "title":title,
                "queryset":queryset,
                "responses":responses
    }
    return render(request, "data/training/feedback.html" ,context)

# class (ListView):
#     # queryset = DSU.objects.all(type="Staff").order_by("-created_at")
#     queryset=DSU.objects.all().order_by("-created_at")
#     template_name = "management/departments/hr/assessment.html"
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
    template_name = "data/jobroles/job_tracker.html"
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


def training_services(request):
    services = Service.objects.filter(title='Data Analysis')
    title, description = Service.objects.values_list("title", "description").filter(title='Data Analysis').first()
    print(title,description)
    context={
        "services":services,
        "title":title,
        "description":description,
    }
    return render(request, "data/training/services.html",context)


@login_required
def interview_roles(request):
    context={
        "title": "Training",
        "title_letter": "letter",
    }
    return render(request, "data/interview/interview_roles.html",context)