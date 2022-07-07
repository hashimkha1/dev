from django.urls import path


from . import views
from .views import (
    ApplicantDeleteView,
    ApplicantListView,
    TraineeDeleteView,
    TraineeUpdateView,
)

app_name = "application"
urlpatterns = [
    # =============================APPLICATIONS VIEWS=====================================
    path("", views.career, name="career"),
    path("apply/", views.apply, name="apply"),
    # path('applicants/', views.applicantlist, name='applicants'),
    # path('applicants/', ApplicantListView.as_view(), name='applicant-list'),
    path(
        "applicant/<int:pk>/delete/",
        ApplicantDeleteView.as_view(),
        name="applicant-delete",
    ),
    path("applicants/", views.applicantlist, name="applicants"),
    path("interview/", views.interview, name="interview"),
    path("first_interview/", views.first_interview, name="first_interview"),
    # interview sections by karki
    path("first_interview/section_a/", views.FI_sectionA, name="section_a"),
    path("first_interview/section_b/", views.FI_sectionB, name="section_b"),
    path("first_interview/section_c/", views.FI_sectionC, name="section_c"),
    path(
        "uploadinterviewworks/", views.uploadinterviewworks, name="uploadinterviewworks"
    ),
    # path("second_interview/", views.second_interview, name="second_interview"),
    path("orientation/", views.orientation, name="orientation"),
    path("internal_training/", views.internal_training, name="internal"),
    # For Internal Use Only
    path("policy/", views.policy, name="policy"),
    path("policies/", views.policies, name="policies"),
    path("policy/<int:pk>/update/", views.policies, name="policy-update"),
    path("info/", views.info, name="applicant_info"),
    path("trainee/", views.trainee, name="trainee"),
    path("trainees/", views.trainees, name="trainees"),
    path(
        "trainee/<int:pk>/update/", TraineeUpdateView.as_view(), name="trainee-update"
    ),
    path(
        "trainee/<int:pk>/delete/", TraineeDeleteView.as_view(), name="trainee-delete"
    ),
    path("rating/", views.rating, name="rating"),
    path("rate/", views.rate, name="rate"),
    # path('firstupload/', views.firstupload, name='firstupload'),
    # path('fupload/', views.fupload, name='fupload'),
    # path('uploaded/', views.uploaded, name='uploaded'),
    # path('<int:id>/', views.employee_form, name='emp_update'),
    # path('<int:id>/', views.employee_delete, name='emp_delete'),
    # path('employee_list/', views.employee_list, name='emp_list'),
    # path("tinterview/", views.testinterview, name="tinterview"),
    # API data
    # path('applicants', views.applicants, name='applicants'),
    # path('applicationapi/', views.ApplicationDataAPI),
    # path('get_total/', views.get_total),
    # Create activity
    # path('createactivity/', views.createActivity),
    # path('updateapplication/', views.updateApplication),
    # path('deleteapplication/', views.deleteApplication),
]
