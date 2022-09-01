from django.urls import path
from . import views
from .views import (
                        ServicesListView,ServicesDetailView
                     )

app_name = 'testing'
urlpatterns = [
    path('', views.Services_List, name='testing-home'),
    #-----------COMPANY REPORTS---------------------------------------
    path('display/', views.Services_List, name='services'),
    path('interview/<int:pk>', ServicesDetailView.as_view(template_name="testing/resume.html"), name='resume'),
    # path('/services/analysis', ServicesDetailView.as_view(template_name="testing/resume.html"), name='analysis'),
    # path('/services/pmanagement', ServicesDetailView.as_view(template_name="testing/resume.html"), name='pmanagement'),
]  