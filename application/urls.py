from django.urls import path
from . import views
from .views import (
    ApplicantDeleteView,
    TraineeDeleteView,
    TraineeUpdateView,
    TraineeAssessmentCreateView,
    TraineeAssessmentUpdateView
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
   

]
