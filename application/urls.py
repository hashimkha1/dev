from django.urls import path, include
from . import views
from .views import websitewcag_list,websitewcagcreate_view
app_name = 'application'
urlpatterns = [
    # path('application/', include('application.urls')),
    #=============================USERS VIEWS=====================================
    #path('', views.home, name='home'),

    path('wcaglist/', views.websitewcag_list, name='wcaglist'),
    path('openaicreate/', views.websitewcagcreate_view, name='openaicreate'),
    #path('propertyupdate/<int:pk>/',views.company_properties_update,name='propertyupdate'),
    #path('propertydelete/<int:pk>/',views.company_properties_delete,name='propertydelete'),
    #path('propertydetail/<int:pk>/',views.company_properties_detail,name='propertydetail'),
]
