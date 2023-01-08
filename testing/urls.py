from django.urls import path
from . import views
from .views import (
                        ServicesListView,ServicesDetailView
                     )

app_name = 'testing'
urlpatterns = [
    path('', views.Services_List, name='testing-home'),
    path('testing/', views.testing, name='testing-pay'),
    #-----------COMPANY REPORTS---------------------------------------
    path('display/', views.Services_List, name='services'),
    path('interview/<int:pk>', ServicesDetailView.as_view(template_name="testing/resume.html"), name='resume'),
  
    # path(
    #     "newsupplies/",
    #     views.FoodCreateView.as_view(
    #         template_name='main/snippets_templates/generalform.html'
    #     ),
    #     name="newsupplies",
    # ),
    # path(
    #     "newsupplier/",
    #     views.SupplierCreateView.as_view(
    #         template_name='main/snippets_templates/generalform.html'
    #     ),
    #     name="newsupplier",
    # ),
    # path("update/<int:pk>/",views.SupplierUpdateView.as_view(template_name='main/snippets_templates/generalform.html'),name="update-supplier"),
    # path("update/<int:pk>/",views.FoodUpdateView.as_view(template_name='main/snippets_templates/generalform.html'),name="update-food"),
    # path("suppliers/",views.SupplierListView.as_view(),name="suppliers"),
    # path("food/",views.FoodListView.as_view(),name="supplies"),
    # path('/services/analysis', ServicesDetailView.as_view(template_name="testing/resume.html"), name='analysis'),
    # path('/services/pmanagement', ServicesDetailView.as_view(template_name="testing/resume.html"), name='pmanagement'),
    path('all_logs/', views.LogsViewSet, name='all_logs'),
    path('justification/<int:pk>/', views.justification, name='justification'),
    path('add_justification/', views.add_requirement_justification, name='join'),

]  