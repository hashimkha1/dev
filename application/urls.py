from django.urls import path
from . import views
from management.views import policies
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
    path(
        "applicant/<int:pk>/delete/",
        ApplicantDeleteView.as_view(),
        name="applicant-delete",
    ),
    path("applicants/", views.applicantlist, name="applicants"),
    path("dckmembers/", views.applicantlist, name="dckmembers"),
    path("interview/", views.interview, name="interview"),
    path("first_interview/", views.first_interview, name="first_interview"),
    path("firstinterview/", views.firstinterview, name="firstinterview"),
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
    # path("policy/", views.policy, name="policy"),
    path("policies/", views.policies, name="policies"),
    path("reporting/", views.trainee, name="trainee"),
    path("trainees/", views.trainees, name="trainees"),
    path(
        "trainee/<int:pk>/update/", TraineeUpdateView.as_view(), name="trainee-update"
    ),
    path(
        "trainee/<int:pk>/delete/", TraineeDeleteView.as_view(), name="trainee-delete"
    ),
    path("enter_score/", views.enter_score, name="enter_score"),
    path(
        "score/<int:pk>/update/", views.ScoresUpdateView.as_view(), name="score-update"
    ),
    path("rating/", views.rating, name="rating"),
    path("rating/<str:username>", views.userscores, name="userscores"),
    path("rate/", views.rate, name="rate"),
    path("rate/<str:pk>", views.ratewid, name="ratewid"),

]
