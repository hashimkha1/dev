from django.urls import path
from . import views
from .views import (
                    RequirementListView,RequirementCreateView, RequirementUpdateView,List           
                    )
app_name = 'accounts'
urlpatterns = [
    #=============================USERS VIEWS=====================================
    path('', views.home, name='home'),
  #  path('requrements/', views.requirementList, name='requrements'),
     path('requirements/', RequirementListView.as_view(), name='requirements'),
     path('requirements/new/', RequirementCreateView.as_view(), name='requirement_create'),
     path('requirements/<int:pk>/update/', RequirementUpdateView.as_view(), name='requirement_update'),
     path('Listv/', views.List, name='Listv'),
]