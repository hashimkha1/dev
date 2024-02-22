from django.urls import path, include
from . import views
from .views import codawebsite_list_view,codawebsitecreate_view
app_name = 'application'
urlpatterns = [
    # path('application/', include('application.urls')),
    #=============================USERS VIEWS=====================================
    #path('', views.home, name='home'),

    path('wcaglist/', views.codawebsite_list_view, name='wcaglist'),
    path('openaicreate/', views.codawebsitecreate_view, name='openaicreate'),
    #path('propertyupdate/<int:pk>/',views.company_properties_update,name='propertyupdate'),
    #path('propertydelete/<int:pk>/',views.company_properties_delete,name='propertydelete'),
    #path('propertydetail/<int:pk>/',views.company_properties_detail,name='propertydetail'),

]