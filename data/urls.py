from django.urls import path
from data import views
from data.views import (
    FeaturedCategoryCreateView,
    FeaturedSubCategoryCreateView,
    FeaturedActivityCreateView,
    FeaturedActivityLinksCreateView,
    FeaturedCategoryUpdateView,
    FeaturedSubCategoryUpdateView,
    FeaturedActivityUpdateView,
    FeaturedActivityLinksUpdateView,
    FeaturedCategoryDeleteView,
    FeaturedSubCategoryDeleteView,
    FeaturedActivityDeleteView,
    FeaturedActivityLinksDeleteView,
    DSUListView,
    LinksListView,
    RoleUpdateView,
    InterviewDetailView,
    InterviewUpdateView,
    InterviewDeleteView,
    InterviewListView,
    InterviewCreateView,
    JobCreateView,
    JobListView,
    InterviewQuestionListView
)

app_name = "data"
urlpatterns = [
    path("", views.analysis, name="home"),
    path("report/", views.report, name="report"),
    path("etl/", views.etl, name="etl"),
    path("database/", views.database, name="database"),
    path("financialsystem/", views.financialsystem, name="finance"),
    path("payroll/", views.payroll, name="payroll"),
    path("project/", views.project, name="project"),
    path("employetraining/", views.employetraining, name="employeetraining"),
    path("employetrainig/updatelinks", views.updatelinks_employetraining, name="updatelinks_employetraining"),
    # Training SEction Urls starts
    path("training/", views.training, name="training"),
    path("train/", views.TrainingView.as_view(), name="train"),
    path("course/", views.CourseView.as_view(), name="course"),
    path("training_v2/", views.training_v2, name="training_v2"),
    path("bitraining/", views.bitraining, name="bitraining"),
    path("bitraining2/", views.activity_view, name="bitraining2"),
    path("updatelist/", views.table_activity_view, name="activity-list"),
    path("links/", views.LinksListView.as_view(), name="listlinks"),
    path("bi_training/", views.bi_training, name="bi_training"),
    path("role/", views.RoleCreateView.as_view(), name="jobrole"),
    path("roles/", views.RolesView.as_view(), name="jobroles"),
    path("roles/edit/<int:pk>/", views.RoleUpdateView.as_view(), name="role-update"),
    path("roles/delete/<int:pk>/", views.RoleDeleteView.as_view(), name="role-delete"),
    # Interview SEction Urls starts
    path("interview/", views.interview, name="interview"),
    path("interview_progress/", views.RoleListView.as_view(), name="interview_progress"),
    # path("testing/", views.questionview, name="testing"),
    path("interview/<str:question_type>/", views.questionview, name="question-detail"),
    # path("interview/<str:resume>", views.RoleDetailView.as_view, name="detail-resume"),
    # path("interview/<str:introduction>", views.RoleDetailView.as_view, name="detail-introduction"),
    # Interview section urls ends
    path("deliverable/", views.deliverable, name="deliverable"),
    path("getdata/", views.getdata, name="getdata"),
    path("pay/", views.pay, name="pay"),
    # Interview/Assignment Section
    # ----------------------CREATION----------------------------------------------------
    path(
        "uploadinterview/",
        InterviewCreateView.as_view(),
        name="uploadinterview",
    ),
    path(
        "addquestion/",
        views.PrepQuestionsCreateView.as_view(template_name='main/snippets_templates/generalform.html'),
        name="add_question",
    ),

    # path('upload/', views.uploadinterview, name='upload'),
    # ----------------------LISTING----------------------------------------------------
    path("iuploads/", InterviewListView.as_view(), name="interviewlist"),
    path("courseuploads/", InterviewQuestionListView.as_view(), name="questionlist"),
    path("interviewuploads/", views.iuploads, name="interviewuploads"),
    path('prepquestions/', views.prepquestions, name='prepquestions'),
    path("useruploads/", views.useruploads, name="user-list"),
    # path('iuploads/', UploadListView.as_view(), name='iuploads'),
    # path('uploaded/', views.uploaded, name='uploaded'),
    # ----------------------DETAIL----------------------------------------------------
    path(
        "upload/<int:pk>/",
        InterviewDetailView.as_view(
            template_name="data/interview/interviews_detail.html"
        ),
        name="interview-detail",
    ),
    # ----------------------UPDATE----------------------------------------------------
    path(
        "interview/<int:pk>/update",
        InterviewUpdateView.as_view(template_name="data/interview/interview_form.html"),
        name="interview-update",
    ),
    path(
        "questions/<int:pk>/update",
        views.PrepQuestionsUpdateView.as_view(template_name="main/snippets_templates/generalform.html"),
        name="question-update",
    ),
    # ----------------------DELETING----------------------------------------------------
    path(
        "interview/<int:pk>/delete",
        InterviewDeleteView.as_view(
            template_name="data/interview/interview_confirm_delete.html"
        ),
        name="delete-interview",
    ),
    # =============================JOB VIEWS=====================================
    path(
        "newjob/",
        JobCreateView.as_view(template_name="data/interview/interview_form.html"),
        name="job-create",
    ),
    path("job_tracker/", JobListView.as_view(), name="job-list"),
    path("job_tracker/<str:username>/", views.userjobtracker, name="userjoblist"),
    # TRAINING SECTION
    # ----------------------Creation----------------------------------------------------
    path(
        "newcategory/",
        FeaturedCategoryCreateView.as_view(
            template_name="data/training/form_templates/task_form.html"
        ),
        name="featuredcategory",
    ),
    path(
        "newsubcategory/",
        FeaturedSubCategoryCreateView.as_view(
            template_name="data/training/form_templates/task_form.html"
        ),
        name="featuredsubcategory",
    ),
    path(
        "newactivity/",
        FeaturedActivityCreateView.as_view(
            template_name="data/training/form_templates/task_form.html"
        ),
        name="featuredactivity",
    ),
    path(
        "newlink/",
        FeaturedActivityLinksCreateView.as_view(
            template_name="data/training/form_templates/task_form.html"
        ),
        name="featuredlink",
    ),
    # path('dsu/new', DSUCreateView.as_view(template_name='data/training/form_templates/task_form.html'), name='dsu'),
    path("dsu/new", views.dsu_entry, name="dsu_entry"),
    # ----------------------List----------------------------------------------------
    path('<str:title>/', views.categorydetail, name='category-detail'),
    path('subcategory/<str:title>/', views.subcategorydetail, name='subcategory-detail'),
    path('activity/<str:title>/', views.activitydetail, name='activity-detail'),
    path("dsu/", DSUListView.as_view(), name="dsu"),
    
    # ----------------------Update----------------------------------------------------
    path(
        "category/<int:pk>/update",
        FeaturedCategoryUpdateView.as_view(
            template_name="data/training/form_templates/task_form.html"
        ),
        name="update-category",
    ),
    path(
        "subcategory/<int:pk>/update",
        FeaturedSubCategoryUpdateView.as_view(
            template_name="data/training/form_templates/task_form.html"
        ),
        name="update-subcategory",
    ),
    path(
        "activity/<int:pk>/update",
        FeaturedActivityUpdateView.as_view(
            template_name="data/training/form_templates/task_form.html"
        ),
        name="update-activity",
    ),
    path(
        "links/<int:pk>/update",
        FeaturedActivityLinksUpdateView.as_view(
            template_name="data/training/form_templates/task_form.html"
        ),
        name="update-links",
    ),
    # ----------------------Deletion----------------------------------------------------
    path(
        "category/<int:pk>/delete",
        FeaturedCategoryDeleteView.as_view(
            template_name="data/training/delete_templates/task_delete.html"
        ),
        name="delete-category",
    ),
    path(
        "subcategory/<int:pk>/delete",
        FeaturedSubCategoryDeleteView.as_view(
            template_name="data/training/delete_templates/task_delete.html"
        ),
        name="delete-subcategory",
    ),
    path(
        "activity/<int:pk>/delete",
        FeaturedActivityDeleteView.as_view(
            template_name="data/training/delete_templates/task_delete.html"
        ),
        name="delete-activity",
    ),
    path(
        "links/<int:pk>/delete",
        FeaturedActivityLinksDeleteView.as_view(
            template_name="data/training/delete_templates/task_delete.html"
        ),
        name="delete-links",
    ),
]
